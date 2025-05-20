-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create template categories table
CREATE TABLE IF NOT EXISTS template_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create templates table
CREATE TABLE IF NOT EXISTS templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    content JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL CHECK (status IN ('active', 'draft', 'archived')) DEFAULT 'draft',
    category_id UUID REFERENCES template_categories(id) ON DELETE SET NULL,
    created_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user_templates table for tracking user's access to templates
CREATE TABLE IF NOT EXISTS user_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    template_id UUID REFERENCES templates(id) ON DELETE CASCADE,
    can_edit BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, template_id)
);

-- Create messages table for chat history
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    sender TEXT NOT NULL CHECK (sender IN ('user', 'assistant')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Set up Row Level Security (RLS)
-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE template_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Create policies for profiles
CREATE POLICY "Users can view their own profile" 
    ON profiles FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" 
    ON profiles FOR UPDATE 
    USING (auth.uid() = id);

-- Create policies for template_categories
CREATE POLICY "Template categories are viewable by everyone" 
    ON template_categories FOR SELECT 
    USING (true);

-- Create policies for templates
CREATE POLICY "Public templates are viewable by everyone" 
    ON templates FOR SELECT 
    USING (is_public = true);

CREATE POLICY "Users can view templates they have access to" 
    ON templates FOR SELECT 
    USING (
        EXISTS (
            SELECT 1 FROM user_templates 
            WHERE user_templates.template_id = templates.id 
            AND user_templates.user_id = auth.uid()
        )
        OR created_by = auth.uid()
    );

CREATE POLICY "Users can insert their own templates" 
    ON templates FOR INSERT 
    WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Users can update templates they created" 
    ON templates FOR UPDATE 
    USING (auth.uid() = created_by);

CREATE POLICY "Users can update templates they have edit access to" 
    ON templates FOR UPDATE 
    USING (
        EXISTS (
            SELECT 1 FROM user_templates 
            WHERE user_templates.template_id = templates.id 
            AND user_templates.user_id = auth.uid()
            AND user_templates.can_edit = true
        )
    );

CREATE POLICY "Users can delete templates they created" 
    ON templates FOR DELETE 
    USING (auth.uid() = created_by);

-- Create policies for user_templates
CREATE POLICY "Users can view their template access" 
    ON user_templates FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Template creators can manage access" 
    ON user_templates FOR ALL 
    USING (
        EXISTS (
            SELECT 1 FROM templates 
            WHERE templates.id = user_templates.template_id 
            AND templates.created_by = auth.uid()
        )
    );

-- Create policies for messages
CREATE POLICY "Users can view their own messages" 
    ON messages FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own messages" 
    ON messages FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Create functions and triggers
-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers to automatically update the updated_at column
CREATE TRIGGER update_profiles_updated_at
BEFORE UPDATE ON profiles
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_template_categories_updated_at
BEFORE UPDATE ON template_categories
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_templates_updated_at
BEFORE UPDATE ON templates
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
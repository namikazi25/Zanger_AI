// Template types
export type Template = {
  id: string;
  title: string;
  status: "active" | "draft" | "archived";
  description: string;
};

export type TemplateCategory = {
  id: string;
  name: string;
  templates: Template[];
};

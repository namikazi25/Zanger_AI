"use client";

import { Fragment, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Menu, Transition } from "@headlessui/react";
import { Bars3Icon, ChevronDownIcon } from "@heroicons/react/24/outline";
import { useSupabase } from "@/components/providers/supabase-provider";
import type { User } from "@supabase/supabase-js";

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

interface HeaderProps {
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

export default function Header({ sidebarOpen, setSidebarOpen }: HeaderProps) {
  const router = useRouter();
  const { supabase } = useSupabase();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch current user
  useEffect(() => {
    const getUser = async () => {
      try {
        const {
          data: { user },
          error,
        } = await supabase.auth.getUser();
        if (error) {
          console.error("Error fetching user:", error);
        } else {
          setUser(user);
        }
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setLoading(false);
      }
    };

    getUser();

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, [supabase.auth]);

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    router.push("/auth/login");
  };

  // Generic avatar component
  const Avatar = ({
    name = "User",
    size = 32,
  }: {
    name?: string;
    size?: number;
  }) => {
    const initials = name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);

    return (
      <div
        className="bg-primary-600 text-white rounded-full flex items-center justify-center font-medium"
        style={{ width: size, height: size, fontSize: size * 0.4 }}
      >
        {initials}
      </div>
    );
  };

  // Extract user display name
  const getUserDisplayName = () => {
    if (!user) return "User";

    // Try to get name from user metadata
    if (user.user_metadata?.full_name) {
      return user.user_metadata.full_name;
    }

    // Try to get name from user metadata (alternative fields)
    if (user.user_metadata?.name) {
      return user.user_metadata.name;
    }

    // Try to construct name from first_name and last_name
    if (user.user_metadata?.first_name || user.user_metadata?.last_name) {
      const firstName = user.user_metadata.first_name || "";
      const lastName = user.user_metadata.last_name || "";
      return `${firstName} ${lastName}`.trim();
    }

    // Fallback to email username
    if (user.email) {
      return user.email.split("@")[0];
    }

    return "User";
  };

  // Extract user email
  const getUserEmail = () => {
    return user?.email || "";
  };

  const displayName = getUserDisplayName();
  const userEmail = getUserEmail();

  return (
    <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-primary-200 bg-white/80 backdrop-blur-sm px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
      <button
        type="button"
        className="-m-2.5 p-2.5 text-primary-700 lg:hidden"
        onClick={() => setSidebarOpen(true)}
      >
        <span className="sr-only">Open sidebar</span>
        <Bars3Icon className="h-6 w-6" aria-hidden="true" />
      </button>

      {/* Separator */}
      <div className="h-6 w-px bg-primary-200 lg:hidden" aria-hidden="true" />

      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div className="flex-1" />
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          {/* Profile dropdown */}
          <Menu as="div" className="relative">
            <Menu.Button className="-m-1.5 flex items-center p-1.5">
              <span className="sr-only">Open user menu</span>
              {loading ? (
                <div className="h-8 w-8 bg-primary-200 rounded-full animate-pulse" />
              ) : (
                <Avatar name={displayName} size={32} />
              )}
              <span className="hidden lg:flex lg:items-center">
                <div className="ml-4">
                  <div className="text-sm font-semibold leading-6 text-primary-900 text-left">
                    {loading ? "Loading..." : displayName}
                  </div>
                  {userEmail && (
                    <div className="text-xs text-primary-600">{userEmail}</div>
                  )}
                </div>
                <ChevronDownIcon
                  className="ml-2 h-5 w-5 text-primary-400"
                  aria-hidden="true"
                />
              </span>
            </Menu.Button>
            <Transition
              as={Fragment}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 z-10 mt-2.5 w-48 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-primary-900/5 focus:outline-none">
                {/* User info header */}
                <div className="px-3 py-2 border-b border-primary-100">
                  <div className="text-sm font-medium text-primary-900">
                    {displayName}
                  </div>
                  {userEmail && (
                    <div className="text-xs text-primary-600 truncate">
                      {userEmail}
                    </div>
                  )}
                </div>

                <Menu.Item>
                  {({ active }) => (
                    <Link
                      href="/profile"
                      className={classNames(
                        active ? "bg-primary-50" : "",
                        "block px-3 py-2 text-sm leading-6 text-primary-900"
                      )}
                    >
                      Your profile
                    </Link>
                  )}
                </Menu.Item>
                <Menu.Item>
                  {({ active }) => (
                    <Link
                      href="/settings"
                      className={classNames(
                        active ? "bg-primary-50" : "",
                        "block px-3 py-2 text-sm leading-6 text-primary-900"
                      )}
                    >
                      Settings
                    </Link>
                  )}
                </Menu.Item>
                <div className="border-t border-primary-100 my-1" />
                <Menu.Item>
                  {({ active }) => (
                    <button
                      onClick={handleSignOut}
                      className={classNames(
                        active ? "bg-primary-50" : "",
                        "block w-full text-left px-3 py-2 text-sm leading-6 text-primary-900"
                      )}
                    >
                      Sign out
                    </button>
                  )}
                </Menu.Item>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
    </div>
  );
}

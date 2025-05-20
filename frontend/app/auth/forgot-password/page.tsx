"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { useSupabase } from "@/components/providers/supabase-provider"
import ZangerLogo from "@/components/zanger-logo"

export default function ForgotPasswordPage() {
  const { supabase } = useSupabase()
  const [email, setEmail] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/auth/reset-password`,
      })

      if (error) throw error
      setSuccess(true)
    } catch (error: any) {
      setError(error.message || "An error occurred while sending the reset link")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gray-50">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <ZangerLogo className="w-16 h-16" />
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Reset your password</h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Or{" "}
          <Link href="/auth/login" className="font-medium text-blue-600 hover:text-blue-500">
            go back to login
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {error && <div className="mb-4 bg-red-50 text-red-700 p-3 rounded-md text-sm">{error}</div>}

          {success ? (
            <div className="text-center">
              <div className="mb-4 bg-green-50 text-green-700 p-3 rounded-md text-sm">
                Password reset link sent! Check your email.
              </div>
              <p className="mb-4 text-gray-700">
                We've sent a password reset link to <strong>{email}</strong>.
              </p>
              <p className="mb-6 text-gray-700">If you don't see the email, check your spam folder or junk mail.</p>
              <Link
                href="/auth/login"
                className="inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Back to login
              </Link>
            </div>
          ) : (
            <form className="space-y-6" onSubmit={handleResetPassword}>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email address
                </label>
                <div className="mt-1">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex w-full justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? "Sending..." : "Send reset link"}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}

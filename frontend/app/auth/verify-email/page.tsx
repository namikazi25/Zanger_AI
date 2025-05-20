import Link from "next/link"
import ZangerLogo from "@/components/zanger-logo"

export default function VerifyEmailPage() {
  return (
    <div className="flex min-h-screen flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gray-50">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <ZangerLogo className="w-16 h-16" />
        </div>
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Check your email</h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          We've sent you a verification link to complete your registration
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 text-center">
          <p className="mb-4 text-gray-700">
            Please check your email inbox and click on the verification link to complete your registration.
          </p>
          <p className="mb-6 text-gray-700">If you don't see the email, check your spam folder or junk mail.</p>
          <Link
            href="/auth/login"
            className="inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Back to login
          </Link>
        </div>
      </div>
    </div>
  )
}

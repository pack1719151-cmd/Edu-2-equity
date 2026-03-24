"use client"

import * as React from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { useForm, ControllerRenderProps, ControllerFieldState, UseFormStateReturn, FieldValues } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { LogIn, BookOpen, Mail, Lock, Eye, EyeOff } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { authApi } from "@/lib/api-client"

const loginSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
})

type LoginFormValues = z.infer<typeof loginSchema>

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [isLoading, setIsLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [showPassword, setShowPassword] = React.useState(false)
  const [registered, setRegistered] = React.useState(false)

  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: searchParams?.get('email') || "",
      password: "",
    },
  })

  React.useEffect(() => {
    if (searchParams?.get('registered')) {
      setRegistered(true)
      const timer = setTimeout(() => setRegistered(false), 5000)
      return () => clearTimeout(timer)
    }
  }, [searchParams])

  async function onSubmit(data: LoginFormValues) {
    setIsLoading(true)
    setError(null)

    try {
      await authApi.login(data.email, data.password)
      
      // Wait a bit for cookies to be set
      await new Promise(resolve => setTimeout(resolve, 200))
      
      const roleCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('user_role='))
        ?.split('=')[1]
      
      const dashboardRoutes: Record<string, string> = {
        student: "/dashboard/student",
        teacher: "/dashboard/teacher",
        principal: "/dashboard/principal",
      }
      
      const redirectUrl = dashboardRoutes[roleCookie || ''] || "/dashboard"
      router.push(redirectUrl)
      router.refresh()
    } catch (err) {
      const axiosError = err as { response?: { data?: { detail?: string } }; message?: string }
      const backendError = axiosError.response?.data?.detail || axiosError.message || "Invalid email or password"
      setError(backendError)
      console.error("Login error:", err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center shadow-lg">
              <BookOpen className="h-6 w-6 text-white" />
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">EduEquity OS</div>
              <div className="text-sm text-gray-600">Educational Equity Platform</div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-0">
        {/* Left side - Features */}
        <div className="hidden lg:flex flex-col justify-between p-16 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 border-r border-gray-100">
          <div className="space-y-12">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">Welcome Back</h2>
              <p className="text-lg text-gray-700 leading-relaxed">
                Sign in to access your personalized dashboard and manage your educational experience.
              </p>
            </div>

            {/* Features */}
            <div className="space-y-6">
              <div className="flex items-start space-x-4 group">
                <div className="flex-shrink-0 w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200 transition">
                  <div className="w-6 h-6 text-blue-600 font-bold text-lg">✓</div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Real-time Attendance</h3>
                  <p className="text-sm text-gray-600 mt-1">Track attendance with QR codes and live updates</p>
                </div>
              </div>

              <div className="flex items-start space-x-4 group">
                <div className="flex-shrink-0 w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center group-hover:bg-indigo-200 transition">
                  <div className="w-6 h-6 text-indigo-600 font-bold text-lg">✓</div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Interactive Quizzes</h3>
                  <p className="text-sm text-gray-600 mt-1">Create and manage engaging quiz assessments</p>
                </div>
              </div>

              <div className="flex items-start space-x-4 group">
                <div className="flex-shrink-0 w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center group-hover:bg-purple-200 transition">
                  <div className="w-6 h-6 text-purple-600 font-bold text-lg">✓</div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Advanced Analytics</h3>
                  <p className="text-sm text-gray-600 mt-1">Gain insights with comprehensive dashboards</p>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-200 pt-8">
            <p className="text-gray-700">
              Don&apos;t have an account?{' '}
              <Link href="/register" className="font-semibold text-blue-600 hover:text-blue-700">
                Create one now
              </Link>
            </p>
          </div>
        </div>

        {/* Right side - Form */}
        <div className="flex flex-col justify-center px-4 py-12 sm:px-6 lg:px-8">
          <div className="w-full max-w-md mx-auto">
            {/* Mobile header */}
            <div className="lg:hidden mb-10 text-center">
              <div className="flex items-center justify-center space-x-3 mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center shadow-lg">
                  <BookOpen className="h-6 w-6 text-white" />
                </div>
                <span className="text-2xl font-bold text-gray-900">EduEquity</span>
              </div>
              <p className="text-gray-600 text-sm">Educational Equity Platform</p>
            </div>

            {/* Success message */}
            {registered && (
              <div className="mb-6 rounded-xl bg-green-50 border border-green-200 p-4">
                <div className="flex items-center space-x-3">
                  <div className="text-green-600 text-xl">✓</div>
                  <div>
                    <div className="font-semibold text-green-900">Account created successfully!</div>
                    <div className="text-sm text-green-800">Now sign in with your credentials</div>
                  </div>
                </div>
              </div>
            )}

            <div className="space-y-8">
              <div className="text-center">
                <h1 className="text-3xl font-bold text-gray-900">Sign in</h1>
                <p className="text-gray-600 mt-2">Access your dashboard and continue your journey</p>
              </div>

              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                  {error && (
                    <div className="rounded-xl bg-red-50 border border-red-200 p-4">
                      <div className="flex items-start space-x-3">
                        <div className="text-red-600 text-xl">⚠</div>
                        <div>
                          <div className="font-semibold text-red-900">Sign in failed</div>
                          <p className="text-sm text-red-800 mt-1">{error}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  <FormField
                    control={form.control}
                    name="email"
                    render={(props: any) => (
                      <FormItem>
                        <FormLabel className="text-sm font-semibold text-gray-900">Email Address</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Mail className="absolute left-4 top-4 h-5 w-5 text-gray-400" />
                            <Input
                              type="email"
                              placeholder="you@example.com"
                              disabled={isLoading}
                              className="pl-12 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500 rounded-lg text-gray-900 placeholder-gray-500"
                              {...props.field}
                            />
                          </div>
                        </FormControl>
                        <FormMessage className="text-red-600 text-sm mt-1" />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="password"
                    render={(props: any) => (
                      <FormItem>
                        <div className="flex items-center justify-between">
                          <FormLabel className="text-sm font-semibold text-gray-900">Password</FormLabel>
                          <a href="#" className="text-sm text-blue-600 hover:text-blue-700 font-medium">Forgot password?</a>
                        </div>
                        <FormControl>
                          <div className="relative">
                            <Lock className="absolute left-4 top-4 h-5 w-5 text-gray-400" />
                            <Input
                              type={showPassword ? "text" : "password"}
                              placeholder="Enter your password"
                              disabled={isLoading}
                              className="pl-12 pr-12 h-12 border-gray-300 focus:border-blue-500 focus:ring-blue-500 rounded-lg text-gray-900 placeholder-gray-500"
                              {...props.field}
                            />
                            <button
                              type="button"
                              onClick={() => setShowPassword(!showPassword)}
                              className="absolute right-4 top-4 text-gray-400 hover:text-gray-600 transition"
                            >
                              {showPassword ? (
                                <EyeOff className="h-5 w-5" />
                              ) : (
                                <Eye className="h-5 w-5" />
                              )}
                            </button>
                          </div>
                        </FormControl>
                        <FormMessage className="text-red-600 text-sm mt-1" />
                      </FormItem>
                    )}
                  />

                  <div className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      id="remember"
                      className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                    />
                    <label htmlFor="remember" className="text-sm text-gray-700 font-medium cursor-pointer">
                      Remember me for 30 days
                    </label>
                  </div>

                  <Button
                    type="submit"
                    className="w-full h-12 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-lg shadow-blue-600/20 transition duration-200 flex items-center justify-center"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <div className="animate-spin mr-2 h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                        Signing in...
                      </>
                    ) : (
                      <>
                        <LogIn className="mr-2 h-5 w-5" />
                        Sign in to Dashboard
                      </>
                    )}
                  </Button>
                </form>
              </Form>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-200"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">New to EduEquity?</span>
                </div>
              </div>

              <Link
                href="/register"
                className="w-full h-12 border-2 border-gray-300 hover:border-gray-400 text-gray-900 font-semibold rounded-lg transition duration-200 flex items-center justify-center bg-gray-50 hover:bg-gray-100"
              >
                Create a free account
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

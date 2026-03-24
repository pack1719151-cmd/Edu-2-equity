"use client"

import * as React from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useForm, ControllerRenderProps, ControllerFieldState, UseFormStateReturn } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { UserPlus, BookOpen, Mail, Lock, User2, GraduationCap, Eye, EyeOff } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { authApi } from "@/lib/api-client"

const registerSchema = z.object({
  full_name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
  confirmPassword: z.string(),
  role: z.enum(["student", "teacher", "principal"], {
    required_error: "Please select a role",
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
})

type RegisterFormValues = z.infer<typeof registerSchema>

export default function RegisterPage() {
  const router = useRouter()
  const [isLoading, setIsLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [showPassword, setShowPassword] = React.useState(false)
  const [showConfirm, setShowConfirm] = React.useState(false)

  const form = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      full_name: "",
      email: "",
      password: "",
      confirmPassword: "",
      role: "student",
    },
  })

  async function onSubmit(data: RegisterFormValues) {
    setIsLoading(true)
    setError(null)

    try {
      const result = await authApi.register({
        email: data.email,
        password: data.password,
        full_name: data.full_name,
        role: data.role,
      })

      if (result.success) {
        // Redirect to login with email pre-filled
        router.push(`/login?email=${encodeURIComponent(data.email)}&registered=true`)
      } else {
        setError(result.message || "Registration failed. Please try again.")
      }
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: { detail?: string } }; message?: string }
      const backendError = axiosError.response?.data?.detail || axiosError.message || "An error occurred during registration"
      setError(backendError)
      console.error("Register error:", err)
    } finally {
      setIsLoading(false)
    }
  }

  const roleOptions = [
    { value: "student", label: "Student", icon: GraduationCap, color: "blue", bgColor: "bg-blue-50", borderColor: "border-blue-500", textColor: "text-blue-600" },
    { value: "teacher", label: "Teacher", icon: BookOpen, color: "green", bgColor: "bg-green-50", borderColor: "border-green-500", textColor: "text-green-600" },
    { value: "principal", label: "Principal", icon: User2, color: "purple", bgColor: "bg-purple-50", borderColor: "border-purple-500", textColor: "text-purple-600" },
  ]

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-br from-green-600 to-emerald-700 rounded-xl flex items-center justify-center shadow-lg">
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
        <div className="hidden lg:flex flex-col justify-between p-16 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 border-r border-gray-100">
          <div className="space-y-12">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">Join Our Community</h2>
              <p className="text-lg text-gray-700 leading-relaxed">
                Create your account and unlock access to personalized learning tools, real-time collaboration, and advanced analytics.
              </p>
            </div>

            {/* Features */}
            <div className="space-y-6">
              <div className="flex items-start space-x-4 group">
                <div className="flex-shrink-0 w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200 transition">
                  <GraduationCap className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">For Students</h3>
                  <p className="text-sm text-gray-600 mt-1">Track attendance, attempt quizzes, and monitor your progress</p>
                </div>
              </div>

              <div className="flex items-start space-x-4 group">
                <div className="flex-shrink-0 w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center group-hover:bg-green-200 transition">
                  <BookOpen className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">For Teachers</h3>
                  <p className="text-sm text-gray-600 mt-1">Create quizzes, manage classes, and view detailed analytics</p>
                </div>
              </div>

              <div className="flex items-start space-x-4 group">
                <div className="flex-shrink-0 w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center group-hover:bg-purple-200 transition">
                  <User2 className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">For Principals</h3>
                  <p className="text-sm text-gray-600 mt-1">Monitor school performance, view reports, and manage institutions</p>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-200 pt-8">
            <p className="text-gray-700">
              Already have an account?{' '}
              <Link href="/login" className="font-semibold text-green-600 hover:text-green-700">
                Sign in here
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
                <div className="w-12 h-12 bg-gradient-to-br from-green-600 to-emerald-700 rounded-xl flex items-center justify-center shadow-lg">
                  <BookOpen className="h-6 w-6 text-white" />
                </div>
                <span className="text-2xl font-bold text-gray-900">EduEquity</span>
              </div>
              <p className="text-gray-600 text-sm">Educational Equity Platform</p>
            </div>

            <div className="space-y-8">
              <div className="text-center">
                <h1 className="text-3xl font-bold text-gray-900">Create Account</h1>
                <p className="text-gray-600 mt-2">Join thousands of educators and students</p>
              </div>

              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                  {error && (
                    <div className="rounded-xl bg-red-50 border border-red-200 p-4">
                      <div className="flex items-start space-x-3">
                        <div className="text-red-600 text-xl">⚠</div>
                        <div>
                          <div className="font-semibold text-red-900">Registration failed</div>
                          <p className="text-sm text-red-800 mt-1">{error}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  <FormField
                    control={form.control}
                    name="full_name"
                    render={(props: any) => (
                      <FormItem>
                        <FormLabel className="text-sm font-semibold text-gray-900">Full Name</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <User2 className="absolute left-4 top-4 h-5 w-5 text-gray-400" />
                            <Input
                              placeholder="John Doe"
                              disabled={isLoading}
                              className="pl-12 h-12 border-gray-300 focus:border-green-500 focus:ring-green-500 rounded-lg text-gray-900 placeholder-gray-500"
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
                              className="pl-12 h-12 border-gray-300 focus:border-green-500 focus:ring-green-500 rounded-lg text-gray-900 placeholder-gray-500"
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
                    name="role"
                    render={(props: any) => (
                      <FormItem>
                        <FormLabel className="text-sm font-semibold text-gray-900 block mb-3">Select Your Role</FormLabel>
                        <FormControl>
                          <div className="grid grid-cols-3 gap-3">
                            {roleOptions.map((option) => {
                              const Icon = option.icon
                              const isSelected = props.field.value === option.value

                              return (
                                <button
                                  key={option.value}
                                  type="button"
                                  onClick={() => props.field.onChange(option.value)}
                                  className={`flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all duration-200 ${
                                    isSelected
                                      ? `${option.bgColor} ${option.borderColor}`
                                      : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                                  }`}
                                >
                                  <Icon className={`h-6 w-6 mb-2 ${isSelected ? option.textColor : 'text-gray-400'}`} />
                                  <span className={`text-xs font-semibold ${isSelected ? option.textColor : 'text-gray-700'}`}>
                                    {option.label}
                                  </span>
                                </button>
                              )
                            })}
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
                        <FormLabel className="text-sm font-semibold text-gray-900">Password</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Lock className="absolute left-4 top-4 h-5 w-5 text-gray-400" />
                            <Input
                              type={showPassword ? "text" : "password"}
                              placeholder="Minimum 6 characters"
                              disabled={isLoading}
                              className="pl-12 pr-12 h-12 border-gray-300 focus:border-green-500 focus:ring-green-500 rounded-lg text-gray-900 placeholder-gray-500"
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

                  <FormField
                    control={form.control}
                    name="confirmPassword"
                    render={(props: any) => (
                      <FormItem>
                        <FormLabel className="text-sm font-semibold text-gray-900">Confirm Password</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Lock className="absolute left-4 top-4 h-5 w-5 text-gray-400" />
                            <Input
                              type={showConfirm ? "text" : "password"}
                              placeholder="Re-enter your password"
                              disabled={isLoading}
                              className="pl-12 pr-12 h-12 border-gray-300 focus:border-green-500 focus:ring-green-500 rounded-lg text-gray-900 placeholder-gray-500"
                              {...props.field}
                            />
                            <button
                              type="button"
                              onClick={() => setShowConfirm(!showConfirm)}
                              className="absolute right-4 top-4 text-gray-400 hover:text-gray-600 transition"
                            >
                              {showConfirm ? (
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

                  <div className="flex items-start space-x-2">
                    <input
                      type="checkbox"
                      id="terms"
                      className="h-5 w-5 rounded border-gray-300 text-green-600 focus:ring-green-500 cursor-pointer mt-1"
                    />
                    <label htmlFor="terms" className="text-sm text-gray-700 font-medium cursor-pointer">
                      I agree to the{' '}
                      <a href="#" className="text-green-600 hover:text-green-700 font-semibold">Terms of Service</a>{' '}
                      and{' '}
                      <a href="#" className="text-green-600 hover:text-green-700 font-semibold">Privacy Policy</a>
                    </label>
                  </div>

                  <Button
                    type="submit"
                    className="w-full h-12 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg shadow-lg shadow-green-600/20 transition duration-200 flex items-center justify-center"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <div className="animate-spin mr-2 h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                        Creating account...
                      </>
                    ) : (
                      <>
                        <UserPlus className="mr-2 h-5 w-5" />
                        Create Account
                      </>
                    )}
                  </Button>
                </form>
              </Form>

              <div className="relative border-t border-gray-200 pt-6">
                <p className="text-center text-gray-700">
                  Already have an account?{' '}
                  <Link href="/login" className="font-semibold text-green-600 hover:text-green-700">
                    Sign in
                  </Link>
                </p>
              </div>

              <p className="text-xs text-gray-500 text-center">
                🔒 Your data is encrypted and secure. We respect your privacy.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Paths that don't require authentication
const publicPaths = ['/login', '/register', '/api/v1/auth/login', '/api/v1/auth/register']

// Role-based dashboard routes
const roleDashboardRoutes: Record<string, string> = {
  student: '/dashboard/student',
  teacher: '/dashboard/teacher',
  principal: '/dashboard/principal',
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Check if the path is public (no auth required)
  const isPublicPath = publicPaths.some(path =>
    pathname.startsWith(path)
  )

  // Get auth cookies
  const authCookie = request.cookies.get('eduequity_session')
  const userRole = request.cookies.get('user_role')

  // If the path is not public and there's no auth cookie, redirect to login
  if (!isPublicPath && !authCookie) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('redirect', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // If the user is logged in and trying to access login/register, redirect to dashboard
  if ((pathname === '/login' || pathname === '/register') && authCookie) {
    // Redirect to role-based dashboard
    const dashboardUrl = userRole
      ? roleDashboardRoutes[userRole.value] || '/dashboard'
      : '/dashboard'
    return NextResponse.redirect(new URL(dashboardUrl, request.url))
  }

  // Check if user is trying to access a protected route
  if (!isPublicPath && authCookie) {
    // Check for role-based access to dashboard subpaths
    if (pathname.startsWith('/dashboard')) {
      // Allow access to root /dashboard
      if (pathname === '/dashboard') {
        // Redirect to role-specific dashboard
        const dashboardUrl = userRole
          ? roleDashboardRoutes[userRole.value] || '/dashboard'
          : '/dashboard'
        return NextResponse.redirect(new URL(dashboardUrl, request.url))
      }

      // Check if the user has the right role for this dashboard
      if (pathname.startsWith('/dashboard/student') && userRole?.value !== 'student') {
        const dashboardUrl = userRole
          ? roleDashboardRoutes[userRole.value] || '/dashboard'
          : '/dashboard'
        return NextResponse.redirect(new URL(dashboardUrl, request.url))
      }

      if (pathname.startsWith('/dashboard/teacher') && userRole?.value !== 'teacher') {
        const dashboardUrl = userRole
          ? roleDashboardRoutes[userRole.value] || '/dashboard'
          : '/dashboard'
        return NextResponse.redirect(new URL(dashboardUrl, request.url))
      }

      if (pathname.startsWith('/dashboard/principal') && userRole?.value !== 'principal') {
        const dashboardUrl = userRole
          ? roleDashboardRoutes[userRole.value] || '/dashboard'
          : '/dashboard'
        return NextResponse.redirect(new URL(dashboardUrl, request.url))
      }
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     * - api health endpoints
     */
    '/((?!_next/static|_next/image|favicon.ico|public|.*\\.png$|.*\\.jpg$|.*\\.svg$).*)',
  ],
}


// Shared TypeScript types for EduEquity OS

export interface User {
  id: string
  email: string
  full_name: string
  is_active: boolean
  role: 'student' | 'teacher' | 'principal'
  created_at?: string
  updated_at?: string
}

export interface AuthTokens {
  access_token: string
  token_type: string
  refresh_token?: string
}

export interface AttendanceSession {
  id: string
  course_id: string
  date: string
  duration: number
  location?: string
  qr_code?: string
  created_by: string
  created_at?: string
}

export interface AttendanceRecord {
  id: string
  session_id: string
  student_id: string
  status: 'present' | 'absent' | 'late' | 'excused'
  marked_at?: string
}

export interface Quiz {
  id: string
  title: string
  description?: string
  course_id: string
  time_limit?: number
  passing_score?: number
  status: 'draft' | 'published' | 'closed'
  created_by: string
  created_at?: string
  updated_at?: string
}

export interface QuizQuestion {
  id: string
  quiz_id: string
  question: string
  type: 'multiple_choice' | 'true_false' | 'short_answer'
  options?: string[]
  correct_answer: string | string[]
  points: number
}

export interface QuizSubmission {
  id: string
  quiz_id: string
  student_id: string
  answers: Array<{ question_id: string; answer: string | string[] }>
  score?: number
  submitted_at?: string
}

export interface FeedRequest {
  id: string
  type: string
  title: string
  description: string
  status: 'pending' | 'approved' | 'rejected'
  requested_by: string
  related_id?: string
  created_at?: string
  updated_at?: string
}

export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}


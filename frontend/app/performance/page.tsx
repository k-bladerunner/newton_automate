'use client';

import { Layout } from '@/components/layout/Layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { performanceAPI } from '@/lib/api';
import useSWR from 'swr';
import { TrendingUp, Award, Calendar, Flame, BookOpen } from 'lucide-react';

export default function PerformancePage() {
  const { data: overview, isLoading: loadingOverview } = useSWR('/performance/overview', () =>
    performanceAPI.overview().then((res) => res.data)
  );

  const { data: courses, isLoading: loadingCourses } = useSWR('/performance/courses', () =>
    performanceAPI.allCourses().then((res) => res.data)
  );

  const stats = [
    {
      label: 'Lecture Attendance',
      value: `${overview?.lecture_attendance || 0}%`,
      icon: Calendar,
      color: 'text-blue-500',
      bgColor: 'bg-blue-100',
    },
    {
      label: 'Assignments Completed',
      value: `${overview?.assignments_completed || 0}%`,
      icon: TrendingUp,
      color: 'text-green-500',
      bgColor: 'bg-green-100',
    },
    {
      label: 'Total XP Earned',
      value: overview?.total_xp || 0,
      icon: Award,
      color: 'text-yellow-500',
      bgColor: 'bg-yellow-100',
    },
    {
      label: 'Current Streak',
      value: `${overview?.streak_days || 0} days`,
      icon: Flame,
      color: 'text-orange-500',
      bgColor: 'bg-orange-100',
    },
  ];

  return (
    <Layout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Performance Analytics</h1>
          <p className="text-muted-foreground">
            Track your progress and achievements
          </p>
        </div>

        {/* Overall Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {loadingOverview ? (
            <div className="col-span-4 text-center py-12 text-muted-foreground">
              Loading statistics...
            </div>
          ) : (
            stats.map((stat) => {
              const Icon = stat.icon;
              return (
                <Card key={stat.label}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-muted-foreground">{stat.label}</p>
                        <p className="text-3xl font-bold mt-2">{stat.value}</p>
                      </div>
                      <div className={`${stat.bgColor} p-3 rounded-lg`}>
                        <Icon className={`h-6 w-6 ${stat.color}`} />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })
          )}
        </div>

        {/* Course Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Course Performance</CardTitle>
          </CardHeader>
          <CardContent>
            {loadingCourses ? (
              <div className="text-center py-12 text-muted-foreground">
                Loading course performance...
              </div>
            ) : !courses || courses.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground">
                No course data available
              </div>
            ) : (
              <div className="space-y-4">
                {courses.map((course: any) => (
                  <div
                    key={course.course_hash}
                    className="flex items-center justify-between p-4 rounded-lg border"
                  >
                    <div className="flex items-center gap-3">
                      <div className="bg-blue-100 p-2 rounded-lg">
                        <BookOpen className="h-5 w-5 text-blue-500" />
                      </div>
                      <div>
                        <div className="font-medium">{course.course_name}</div>
                        <div className="text-sm text-muted-foreground">
                          Course ID: {course.course_hash.slice(0, 8)}...
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-6 text-sm">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">
                          {course.attendance}%
                        </div>
                        <div className="text-muted-foreground">Attendance</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">
                          {course.assignments}%
                        </div>
                        <div className="text-muted-foreground">Assignments</div>
                      </div>
                      {course.quizzes !== null && (
                        <div className="text-center">
                          <div className="text-2xl font-bold text-purple-600">
                            {course.quizzes}%
                          </div>
                          <div className="text-muted-foreground">Quizzes</div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}

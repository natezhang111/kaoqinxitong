import { createRouter, createWebHistory } from "vue-router";

import AttendanceView from "../views/Attendance.vue";
import AuditLogView from "../views/AuditLog.vue";
import EmotionView from "../views/Emotion.vue";
import GroupPhotoView from "../views/GroupPhoto.vue";
import LoginView from "../views/Login.vue";
import ReportView from "../views/Report.vue";
import SecurityTestView from "../views/SecurityTest.vue";
import StudentManageView from "../views/StudentManage.vue";
import StudentPortalView from "../views/StudentPortal.vue";
import SystemStatusView from "../views/SystemStatus.vue";
import TeacherProfileView from "../views/TeacherProfile.vue";
import UserManageView from "../views/UserManage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/attendance",
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: { public: true },
    },
    {
      path: "/attendance",
      name: "attendance",
      component: AttendanceView,
    },
    {
      path: "/security-tests",
      name: "security-tests",
      component: SecurityTestView,
    },
    {
      path: "/students",
      name: "students",
      component: StudentManageView,
    },
    {
      path: "/student-portal",
      name: "student-portal",
      component: StudentPortalView,
    },
    {
      path: "/users",
      name: "users",
      component: UserManageView,
    },
    {
      path: "/audit-logs",
      name: "audit-logs",
      component: AuditLogView,
    },
    {
      path: "/group-photos",
      name: "group-photos",
      component: GroupPhotoView,
    },
    {
      path: "/emotions",
      name: "emotions",
      component: EmotionView,
    },
    {
      path: "/report",
      name: "report",
      component: ReportView,
    },
    {
      path: "/teacher-profile",
      name: "teacher-profile",
      component: TeacherProfileView,
    },
    {
      path: "/system-status",
      name: "system-status",
      component: SystemStatusView,
    },
  ],
});

router.beforeEach((to) => {
  const token = localStorage.getItem("attendance_token");
  const rawUser = localStorage.getItem("attendance_user");
  let savedUser = null;
  try {
    savedUser = rawUser ? JSON.parse(rawUser) : null;
  } catch {
    savedUser = null;
  }
  if (!to.meta.public && !token) {
    return { name: "login" };
  }
  if (to.name === "login" && token) {
    return { name: savedUser?.role === "student" ? "student-portal" : "attendance" };
  }
  if (
    token &&
    savedUser?.role === "student" &&
    [
      "attendance",
      "students",
      "users",
      "audit-logs",
      "security-tests",
      "group-photos",
      "emotions",
      "report",
      "teacher-profile",
      "system-status",
    ].includes(
      String(to.name || "")
    )
  ) {
    return { name: "student-portal" };
  }
  return true;
});

export default router;

<script setup>
import { useRouter } from "vue-router";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  current: {
    type: String,
    required: true,
  },
  user: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["logout"]);
const router = useRouter();

const navItems = [
  { key: "attendance", label: "考勤" },
  { key: "students", label: "学生管理" },
  { key: "security-tests", label: "安全测试" },
  { key: "group-photos", label: "合照识别" },
<<<<<<< HEAD
  { key: "report", label: "统计报表" },
=======
  { key: "report", label: "活动统计" },
>>>>>>> 98bf8e49 (update)
  { key: "emotions", label: "情绪统计" },
  { key: "users", label: "用户管理" },
  { key: "audit-logs", label: "操作日志" },
  { key: "system-status", label: "系统状态" },
  { key: "teacher-profile", label: "教师中心" },
];

async function navigate(routeName) {
  if (router.currentRoute.value.name === routeName) {
    return;
  }
  await router.push({ name: routeName });
}
</script>

<template>
  <header class="teacher-header">
    <div class="teacher-header-main">
      <div class="teacher-title-block">
        <h1>{{ title }}</h1>
      </div>

      <div class="teacher-account">
        <div class="teacher-user-pill">
          <span>{{ props.user?.username || "未登录" }}</span>
          <small>{{ props.user?.role || "-" }}</small>
        </div>
        <el-button class="teacher-logout-btn" plain @click="emit('logout')">退出登录</el-button>
      </div>
    </div>

    <div class="teacher-header-sub">
      <div class="teacher-nav-grid">
        <el-button
          v-for="item in navItems"
          :key="item.key"
          class="teacher-nav-btn"
          :type="props.current === item.key ? 'primary' : 'default'"
          @click="navigate(item.key)"
        >
          {{ item.label }}
        </el-button>
      </div>

      <div v-if="$slots.actions" class="teacher-header-actions">
        <slot name="actions" />
      </div>
    </div>
  </header>
</template>

<style scoped>
.teacher-header {
  display: grid;
  gap: 16px;
  margin-bottom: 22px;
  padding: 24px 28px;
  border: 1px solid rgba(31, 41, 55, 0.09);
  border-radius: 28px;
  background: rgba(255, 250, 244, 0.82);
  box-shadow: 0 20px 60px rgba(125, 88, 54, 0.12);
  backdrop-filter: blur(12px);
}

.teacher-header-main {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
}

.teacher-title-block {
  min-width: 0;
  flex: 1 1 280px;
}

.teacher-title-block h1 {
  margin: 0;
  font-size: clamp(2rem, 2.6vw, 3rem);
  line-height: 1.08;
  color: #1d2733;
}

.teacher-account {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}

.teacher-user-pill {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  min-width: 112px;
  padding: 12px 14px;
  border-radius: 18px;
  background: rgba(255, 250, 244, 0.85);
  border: 1px solid rgba(31, 41, 55, 0.09);
}

.teacher-user-pill span {
  font-weight: 700;
}

.teacher-user-pill small {
  color: #6c7784;
}

.teacher-header-sub {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
}

.teacher-nav-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  flex: 1 1 760px;
}

:deep(.teacher-nav-btn.el-button) {
  width: 108px;
  min-width: 108px;
  height: 40px;
  margin: 0;
  padding: 0 12px;
  font-weight: 600;
}

.teacher-header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  flex-wrap: wrap;
}

@media (max-width: 960px) {
  .teacher-header {
    padding: 20px;
  }

  .teacher-header-sub {
    flex-direction: column;
    align-items: stretch;
  }

  .teacher-header-actions {
    justify-content: flex-start;
  }
}

@media (max-width: 720px) {
  .teacher-header {
    padding: 18px;
  }

  .teacher-account {
    justify-content: flex-start;
  }

  :deep(.teacher-nav-btn.el-button) {
    width: calc(50% - 5px);
    min-width: 0;
  }
}
</style>

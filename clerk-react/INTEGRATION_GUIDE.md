# 工具集成指南

本项目已成功集成了以下所有工具和库：

## ✅ 已集成的工具

### 路由和状态管理
- **TanStack Router** - 客户端路由系统
- **TanStack Query** - 服务端状态管理和数据获取
- **TanStack Table** - 强大的表格组件

### UI 组件库和样式
- **shadcn/ui 风格组件** - 基于 Radix UI 的组件系统
- **Radix UI** - 无样式组件库（已安装：Avatar、Checkbox、Dialog、Dropdown、Label、Select、Tabs、Tooltip）
- **Tailwind CSS v4** - 最新版本的样式框架
- **@tailwindcss/vite** - Tailwind Vite 插件
- **tw-animate-css** - Tailwind 动画库
- **next-themes** - 主题切换（深色/浅色模式）
- **lucide-react** - 图标库
- **class-variance-authority** - 组件变体管理
- **clsx + tailwind-merge** - 类名工具

### 表单和数据验证
- **React Hook Form** - 表单管理
- **Zod** - 数据验证
- **@hookform/resolvers** - React Hook Form 与 Zod 集成

## 📁 项目结构

```
src/
├── components/
│   ├── ui/
│   │   └── button.tsx          # shadcn/ui 风格的 Button 组件
│   ├── theme-provider.tsx      # 主题提供者
│   ├── theme-toggle.tsx        # 主题切换组件
│   ├── example-form.tsx         # 表单示例（React Hook Form + Zod）
│   └── users-table.tsx         # 表格示例（TanStack Table）
├── hooks/
│   └── use-users.ts            # TanStack Query 数据获取示例
├── lib/
│   ├── utils.ts                # 工具函数（cn 函数）
│   └── query-client.ts         # TanStack Query 客户端配置
├── routes/
│   ├── __root.tsx              # 根路由（包含导航和布局）
│   ├── index.tsx               # 首页
│   ├── about.tsx               # 关于页面
│   ├── users.tsx               # 用户列表页面（展示表格）
│   └── form.tsx                # 表单页面
├── main.tsx                    # 应用入口（集成所有提供者）
└── routeTree.gen.ts            # 自动生成的路由树

```

## 🚀 使用方法

### 1. 启动开发服务器

```bash
pnpm dev
```

开发服务器会自动生成路由类型。

### 2. 构建项目

```bash
pnpm build
```

### 3. 生成路由类型

```bash
pnpm gen:routes
```

## 📝 使用示例

### TanStack Router - 创建新路由

在 `src/routes/` 目录下创建新文件，例如 `src/routes/products.tsx`：

```typescript
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/products')({
  component: Products,
})

function Products() {
  return <div>产品页面</div>
}
```

然后运行 `pnpm gen:routes` 生成路由类型。

### TanStack Query - 数据获取

```typescript
import { useQuery } from '@tanstack/react-query'

function MyComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['myData'],
    queryFn: async () => {
      const res = await fetch('/api/data')
      return res.json()
    },
  })

  if (isLoading) return <div>加载中...</div>
  if (error) return <div>错误: {error.message}</div>
  
  return <div>{JSON.stringify(data)}</div>
}
```

### React Hook Form + Zod - 表单验证

```typescript
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const schema = z.object({
  name: z.string().min(2, "名称至少需要2个字符"),
  email: z.string().email("请输入有效的邮箱"),
})

function MyForm() {
  const form = useForm({
    resolver: zodResolver(schema),
  })

  return (
    <form onSubmit={form.handleSubmit((data) => console.log(data))}>
      <input {...form.register("name")} />
      {form.formState.errors.name && <p>{form.formState.errors.name.message}</p>}
      <button type="submit">提交</button>
    </form>
  )
}
```

### TanStack Table - 表格

参考 `src/components/users-table.tsx` 查看完整示例。

### 使用 UI 组件

```typescript
import { Button } from "@/components/ui/button"

function MyComponent() {
  return (
    <Button variant="default" size="lg">
      点击我
    </Button>
  )
}
```

### 主题切换

主题切换组件已集成在根路由的导航栏中。你也可以在任何组件中使用：

```typescript
import { useTheme } from "next-themes"

function MyComponent() {
  const { theme, setTheme } = useTheme()
  return <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>切换主题</button>
}
```

## 🎨 Tailwind CSS v4 配置

Tailwind CSS v4 使用新的 `@theme` 指令进行配置。主题变量定义在 `src/index.css` 中。

## 📦 路径别名

项目配置了 `@/` 别名指向 `src/` 目录，可以在任何地方使用：

```typescript
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
```

## 🔧 环境变量

确保在 `.env` 文件中设置 Clerk 的发布密钥：

```
VITE_CLERK_PUBLISHABLE_KEY=your_key_here
```

## 📚 更多资源

- [TanStack Router 文档](https://tanstack.com/router)
- [TanStack Query 文档](https://tanstack.com/query)
- [TanStack Table 文档](https://tanstack.com/table)
- [React Hook Form 文档](https://react-hook-form.com)
- [Zod 文档](https://zod.dev)
- [shadcn/ui 文档](https://ui.shadcn.com)
- [Tailwind CSS v4 文档](https://tailwindcss.com)


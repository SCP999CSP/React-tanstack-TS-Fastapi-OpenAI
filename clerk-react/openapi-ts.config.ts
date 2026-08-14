import { defineConfig } from "@hey-api/openapi-ts"

export default defineConfig({
  input: "./openapi.json",
  output: "./src/client",

  plugins: [
    "@hey-api/client-axios",
    {
      name: "@hey-api/sdk",
      operations: {
        strategy: "byTags",
        nesting: "operationId",
        containerName: "{{name}}Service",
        methodName: (operation: any) => {
          // 在新版本中，operation 对象可能包含不同的属性
          // 尝试多种可能的结构
          let name: string = "";
          
          // 尝试不同的属性名
          if (operation?.name) {
            name = operation.name;
          } else if (operation?.operationId) {
            name = operation.operationId;
          } else if (operation?.id) {
            name = operation.id;
          } else if (typeof operation === 'string') {
            name = operation;
          }
          
          // 如果仍然没有找到，尝试从 operation 的其他属性获取
          if (!name && operation) {
            // 打印调试信息（可以在控制台看到实际结构）
            console.log('Operation object:', JSON.stringify(operation, null, 2));
          }
          
          // 从 operationId 中提取方法名
          // operationId 格式: "questions-read_questionslist" -> "readQuestionslist"
          if (name && name.includes('-')) {
            const parts = name.split('-');
            if (parts.length > 1) {
              // 移除服务名前缀（如 "questions-"）
              name = parts.slice(1).join('-');
            }
          }
          
          // 将下划线命名转换为驼峰命名
          // "read_questionslist" -> "readQuestionslist"
          if (name) {
            name = name.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
          }
          
          // 确保 name 不为空
          if (!name || name.length === 0) {
            name = "unknown";
          }

          // 首字母小写
          return name.charAt(0).toLowerCase() + name.slice(1);
        },
      },
    },
    {
      name: "@hey-api/schemas",
      type: "json",
    },
  ],
})
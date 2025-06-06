FROM node:22-alpine AS base

# Install dependencies and build the project.
FROM base AS builder
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine
# to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /app

RUN npm install --ignore-scripts -g pnpm
COPY --chmod=444 package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --ignore-scripts

COPY --chmod=444 .env next.config.ts postcss.config.js tailwind.config.js tsconfig.json ./
COPY --chmod=555 public public
COPY --chmod=555 src src

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm run build

# Production image, copy all the files and run next.
FROM base AS runner
WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs && \
adduser --system --uid 1001 -G nodejs nextjs
# Copying files with root as owner, so that executing user cannot change the container.
COPY --from=builder --chown=root:root --chmod=555 /app/public public

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/pages/api-reference/config/next-config-js/output
COPY --from=builder --chown=root:root --chmod=555  /app/.next/standalone .

# Create cache directory and assign ownership to nextjs user with write permission, so that cache can be stored.
RUN mkdir -p /app/.next/cache && chown -R nextjs:nodejs /app/.next/cache && chmod -R 755 /app/.next/cache
COPY --from=builder --chown=root:root --chmod=555 /app/.next/static .next/static

USER nextjs

EXPOSE 3000

ENV HOSTNAME="0.0.0.0"
ENV PORT=3000

# server.js is created by next build from the standalone output
# https://nextjs.org/docs/pages/api-reference/config/next-config-js/output
CMD ["node", "server.js"]

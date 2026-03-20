import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: text("id").primaryKey(), // Clerk user ID
  email: text("email").notNull(),
  name: text("name"),
  imageUrl: text("image_url"),
  createdAt: integer("created_at", { mode: "timestamp" }).$defaultFn(
    () => new Date(),
  ),
});

export const settings = sqliteTable("settings", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  hotkey: text("hotkey").default("alt+space"),
  language: text("language").default("auto"), // auto | ar | en
  cleanupMode: text("cleanup_mode").default("light"), // light | heavy
  updatedAt: integer("updated_at", { mode: "timestamp" }).$defaultFn(
    () => new Date(),
  ),
});

export const snippets = sqliteTable("snippets", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  trigger: text("trigger").notNull(), // "cal"
  expansion: text("expansion").notNull(), // "calendly.com/eslam"
  createdAt: integer("created_at", { mode: "timestamp" }).$defaultFn(
    () => new Date(),
  ),
});

export const history = sqliteTable("history", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  rawTranscript: text("raw_transcript").notNull(),
  cleanedTranscript: text("cleaned_transcript").notNull(),
  appName: text("app_name"), // "Chrome", "VS Code"
  wordCount: integer("word_count"),
  durationSeconds: integer("duration_seconds"),
  language: text("language"), // "ar" | "en"
  createdAt: integer("created_at", { mode: "timestamp" }).$defaultFn(
    () => new Date(),
  ),
});

export const stats = sqliteTable("stats", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" })
    .unique(),
  totalWords: integer("total_words").default(0),
  totalSessions: integer("total_sessions").default(0),
  totalMinutesSaved: integer("total_minutes_saved").default(0),
  currentStreak: integer("current_streak").default(0),
  lastUsedAt: integer("last_used_at", { mode: "timestamp" }),
  updatedAt: integer("updated_at", { mode: "timestamp" }).$defaultFn(
    () => new Date(),
  ),
});

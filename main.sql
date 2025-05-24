/*
 Navicat Premium Dump SQL

 Source Server         : db_2
 Source Server Type    : SQLite
 Source Server Version : 3045000 (3.45.0)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3045000 (3.45.0)
 File Encoding         : 65001

 Date: 23/05/2025 12:53:41
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS "auth_group";
CREATE TABLE "auth_group" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" varchar(150) NOT NULL,
  UNIQUE ("name" ASC)
);

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS "auth_group_permissions";
CREATE TABLE "auth_group_permissions" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "group_id" integer NOT NULL,
  "permission_id" integer NOT NULL,
  FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS "auth_permission";
CREATE TABLE "auth_permission" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "content_type_id" integer NOT NULL,
  "codename" varchar(100) NOT NULL,
  "name" varchar(255) NOT NULL,
  FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO "auth_permission" VALUES (1, 1, 'add_logentry', 'Can add log entry');
INSERT INTO "auth_permission" VALUES (2, 1, 'change_logentry', 'Can change log entry');
INSERT INTO "auth_permission" VALUES (3, 1, 'delete_logentry', 'Can delete log entry');
INSERT INTO "auth_permission" VALUES (4, 1, 'view_logentry', 'Can view log entry');
INSERT INTO "auth_permission" VALUES (5, 2, 'add_permission', 'Can add permission');
INSERT INTO "auth_permission" VALUES (6, 2, 'change_permission', 'Can change permission');
INSERT INTO "auth_permission" VALUES (7, 2, 'delete_permission', 'Can delete permission');
INSERT INTO "auth_permission" VALUES (8, 2, 'view_permission', 'Can view permission');
INSERT INTO "auth_permission" VALUES (9, 3, 'add_group', 'Can add group');
INSERT INTO "auth_permission" VALUES (10, 3, 'change_group', 'Can change group');
INSERT INTO "auth_permission" VALUES (11, 3, 'delete_group', 'Can delete group');
INSERT INTO "auth_permission" VALUES (12, 3, 'view_group', 'Can view group');
INSERT INTO "auth_permission" VALUES (13, 4, 'add_user', 'Can add user');
INSERT INTO "auth_permission" VALUES (14, 4, 'change_user', 'Can change user');
INSERT INTO "auth_permission" VALUES (15, 4, 'delete_user', 'Can delete user');
INSERT INTO "auth_permission" VALUES (16, 4, 'view_user', 'Can view user');
INSERT INTO "auth_permission" VALUES (17, 5, 'add_contenttype', 'Can add content type');
INSERT INTO "auth_permission" VALUES (18, 5, 'change_contenttype', 'Can change content type');
INSERT INTO "auth_permission" VALUES (19, 5, 'delete_contenttype', 'Can delete content type');
INSERT INTO "auth_permission" VALUES (20, 5, 'view_contenttype', 'Can view content type');
INSERT INTO "auth_permission" VALUES (21, 6, 'add_session', 'Can add session');
INSERT INTO "auth_permission" VALUES (22, 6, 'change_session', 'Can change session');
INSERT INTO "auth_permission" VALUES (23, 6, 'delete_session', 'Can delete session');
INSERT INTO "auth_permission" VALUES (24, 6, 'view_session', 'Can view session');
INSERT INTO "auth_permission" VALUES (25, 7, 'add_userprofile', 'Can add user profile');
INSERT INTO "auth_permission" VALUES (26, 7, 'change_userprofile', 'Can change user profile');
INSERT INTO "auth_permission" VALUES (27, 7, 'delete_userprofile', 'Can delete user profile');
INSERT INTO "auth_permission" VALUES (28, 7, 'view_userprofile', 'Can view user profile');
INSERT INTO "auth_permission" VALUES (29, 8, 'add_mentaldisorder', 'Can add mental disorder');
INSERT INTO "auth_permission" VALUES (30, 8, 'change_mentaldisorder', 'Can change mental disorder');
INSERT INTO "auth_permission" VALUES (31, 8, 'delete_mentaldisorder', 'Can delete mental disorder');
INSERT INTO "auth_permission" VALUES (32, 8, 'view_mentaldisorder', 'Can view mental disorder');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS "auth_user";
CREATE TABLE "auth_user" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "password" varchar(128) NOT NULL,
  "last_login" datetime,
  "is_superuser" bool NOT NULL,
  "username" varchar(150) NOT NULL,
  "last_name" varchar(150) NOT NULL,
  "email" varchar(254) NOT NULL,
  "is_staff" bool NOT NULL,
  "is_active" bool NOT NULL,
  "date_joined" datetime NOT NULL,
  "first_name" varchar(150) NOT NULL,
  UNIQUE ("username" ASC)
);

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO "auth_user" VALUES (1, 'pbkdf2_sha256$1000000$yLdijdKiFKCSEEPBhWN38M$P7mn/kMc5wJS0yYg0oentKh0UqT6cOl3HQP2QLa7WXM=', '2025-05-21 07:54:36.830977', 1, 'hoang', '', 'phanhoang03505@gmail.com', 1, 1, '2025-05-14 14:44:43.864514', '');
INSERT INTO "auth_user" VALUES (2, '$2a123456@123A
123456@123A
$2a$12$Gr3A/NoFz1f6HfJNUTaQ6e9OG7P9k1ai4R1DCEOPWgBSVbSXXUfvC', '2025-05-05', 1, 'hdanhv5879', 'danh', 'hdanhv5879@gmail.com', 1, 1, '2025-05-05', 'danh');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS "auth_user_groups";
CREATE TABLE "auth_user_groups" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "user_id" integer NOT NULL,
  "group_id" integer NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS "auth_user_user_permissions";
CREATE TABLE "auth_user_user_permissions" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "user_id" integer NOT NULL,
  "permission_id" integer NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS "django_admin_log";
CREATE TABLE "django_admin_log" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "object_id" text,
  "object_repr" varchar(200) NOT NULL,
  "action_flag" smallint unsigned NOT NULL,
  "change_message" text NOT NULL,
  "content_type_id" integer,
  "user_id" integer NOT NULL,
  "action_time" datetime NOT NULL,
  FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED,
   ("action_flag" >= 0)
);

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS "django_content_type";
CREATE TABLE "django_content_type" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "app_label" varchar(100) NOT NULL,
  "model" varchar(100) NOT NULL
);

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO "django_content_type" VALUES (1, 'admin', 'logentry');
INSERT INTO "django_content_type" VALUES (2, 'auth', 'permission');
INSERT INTO "django_content_type" VALUES (3, 'auth', 'group');
INSERT INTO "django_content_type" VALUES (4, 'auth', 'user');
INSERT INTO "django_content_type" VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO "django_content_type" VALUES (6, 'sessions', 'session');
INSERT INTO "django_content_type" VALUES (7, 'home', 'userprofile');
INSERT INTO "django_content_type" VALUES (8, 'home', 'mentaldisorder');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS "django_migrations";
CREATE TABLE "django_migrations" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "app" varchar(255) NOT NULL,
  "name" varchar(255) NOT NULL,
  "applied" datetime NOT NULL
);

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO "django_migrations" VALUES (1, 'contenttypes', '0001_initial', '2025-05-14 14:44:21.095003');
INSERT INTO "django_migrations" VALUES (2, 'auth', '0001_initial', '2025-05-14 14:44:21.105460');
INSERT INTO "django_migrations" VALUES (3, 'admin', '0001_initial', '2025-05-14 14:44:21.123387');
INSERT INTO "django_migrations" VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-05-14 14:44:21.131606');
INSERT INTO "django_migrations" VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-14 14:44:21.139833');
INSERT INTO "django_migrations" VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2025-05-14 14:44:21.151866');
INSERT INTO "django_migrations" VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2025-05-14 14:44:21.156258');
INSERT INTO "django_migrations" VALUES (8, 'auth', '0003_alter_user_email_max_length', '2025-05-14 14:44:21.156258');
INSERT INTO "django_migrations" VALUES (9, 'auth', '0004_alter_user_username_opts', '2025-05-14 14:44:21.175773');
INSERT INTO "django_migrations" VALUES (10, 'auth', '0005_alter_user_last_login_null', '2025-05-14 14:44:21.175773');
INSERT INTO "django_migrations" VALUES (11, 'auth', '0006_require_contenttypes_0002', '2025-05-14 14:44:21.190256');
INSERT INTO "django_migrations" VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2025-05-14 14:44:21.196797');
INSERT INTO "django_migrations" VALUES (13, 'auth', '0008_alter_user_username_max_length', '2025-05-14 14:44:21.201791');
INSERT INTO "django_migrations" VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2025-05-14 14:44:21.201791');
INSERT INTO "django_migrations" VALUES (15, 'auth', '0010_alter_group_name_max_length', '2025-05-14 14:44:21.222168');
INSERT INTO "django_migrations" VALUES (16, 'auth', '0011_update_proxy_permissions', '2025-05-14 14:44:21.229862');
INSERT INTO "django_migrations" VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2025-05-14 14:44:21.239516');
INSERT INTO "django_migrations" VALUES (18, 'sessions', '0001_initial', '2025-05-14 14:44:21.245070');
INSERT INTO "django_migrations" VALUES (19, 'home', '0001_initial', '2025-05-14 16:50:38.232315');
INSERT INTO "django_migrations" VALUES (20, 'home', '0002_mentaldisorder', '2025-05-15 08:45:31.243074');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "django_session";
CREATE TABLE "django_session" (
  "session_key" varchar(40) NOT NULL,
  "session_data" text NOT NULL,
  "expire_date" datetime NOT NULL,
  PRIMARY KEY ("session_key")
);

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO "django_session" VALUES ('l7lkqhaa5cxpop4p82nrcuw95wgzzv0s', 'e30:1uFEQU:HR6RAiF3mdiYG-SaIarrkb40mYRoQB2B_6XPvwezm24', '2025-05-28 15:53:46.811534');
INSERT INTO "django_session" VALUES ('lskgg14k29nf7do5bf49sxw5x5vikjjr', '.eJxVjEEOwiAQRe_C2pABO4W6dN8zkBkGpGpoUtqV8e7apAvd_vfef6lA21rC1tISJlEXZdTpd2OKj1R3IHeqt1nHua7LxHpX9EGbHmdJz-vh_h0UauVbkxPxEjshtMTQE1CiKEOXEQwyDkzGm7NxjhL0Dg0we0ALmLMFAfX-AAaFOAQ:1uFFNu:JOdGDIcaTtCLGT_TBs6niSwqzNsqKinw4UVyXRl5dns', '2025-05-28 16:55:10.813324');
INSERT INTO "django_session" VALUES ('cdvm3zf5ev6zcpkw8y9eqqofc1f803bh', '.eJxVjEEOwiAQRe_C2pABO4W6dN8zkBkGpGpoUtqV8e7apAvd_vfef6lA21rC1tISJlEXZdTpd2OKj1R3IHeqt1nHua7LxHpX9EGbHmdJz-vh_h0UauVbkxPxEjshtMTQE1CiKEOXEQwyDkzGm7NxjhL0Dg0we0ALmLMFAfX-AAaFOAQ:1uHeHc:JJzdc4QQ5bfpmUqca0RaLBML5mJlO2R-WtXCipMMqco', '2025-06-04 07:54:36.830977');

-- ----------------------------
-- Table structure for home_mentaldisorder
-- ----------------------------
DROP TABLE IF EXISTS "home_mentaldisorder";
CREATE TABLE "home_mentaldisorder" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "sadness" varchar(100) NOT NULL,
  "euphoric" varchar(100) NOT NULL,
  "exhausted" varchar(100) NOT NULL,
  "sleep_disorder" varchar(100) NOT NULL,
  "mood_swing" varchar(100) NOT NULL,
  "suicidal_thoughts" varchar(100) NOT NULL,
  "anorxia" varchar(100) NOT NULL,
  "authority_respect" varchar(100) NOT NULL,
  "try_explanation" varchar(100) NOT NULL,
  "aggressive_response" varchar(100) NOT NULL,
  "ignore_moveon" varchar(100) NOT NULL,
  "nervous_breakdown" varchar(100) NOT NULL,
  "admit_mistakes" varchar(100) NOT NULL,
  "overthink" varchar(100) NOT NULL,
  "sexual_activity" varchar(100) NOT NULL,
  "concentration" varchar(100) NOT NULL,
  "optimisim" varchar(100) NOT NULL,
  "user_id" integer NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of home_mentaldisorder
-- ----------------------------

-- ----------------------------
-- Table structure for home_userprofile
-- ----------------------------
DROP TABLE IF EXISTS "home_userprofile";
CREATE TABLE "home_userprofile" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "dob" date,
  "gender" varchar(10) NOT NULL,
  "height" real,
  "weight" real,
  "profession" varchar(100),
  "user_id" integer NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED
);

-- ----------------------------
-- Records of home_userprofile
-- ----------------------------
INSERT INTO "home_userprofile" VALUES (1, '2025-05-01', 'Female', 170.0, 60.0, 'Engineer', 1);

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "sqlite_sequence" (
  "name",
  "seq"
);

-- ----------------------------
-- Records of sqlite_sequence
-- ----------------------------
INSERT INTO "sqlite_sequence" VALUES ('django_migrations', 20);
INSERT INTO "sqlite_sequence" VALUES ('django_admin_log', 0);
INSERT INTO "sqlite_sequence" VALUES ('django_content_type', 8);
INSERT INTO "sqlite_sequence" VALUES ('auth_permission', 32);
INSERT INTO "sqlite_sequence" VALUES ('auth_group', 0);
INSERT INTO "sqlite_sequence" VALUES ('auth_user', 2);
INSERT INTO "sqlite_sequence" VALUES ('home_userprofile', 1);

-- ----------------------------
-- Auto increment value for auth_group
-- ----------------------------

-- ----------------------------
-- Indexes structure for table auth_group_permissions
-- ----------------------------
CREATE INDEX "auth_group_permissions_group_id_b120cbf9"
ON "auth_group_permissions" (
  "group_id" ASC
);
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq"
ON "auth_group_permissions" (
  "group_id" ASC,
  "permission_id" ASC
);
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e"
ON "auth_group_permissions" (
  "permission_id" ASC
);

-- ----------------------------
-- Auto increment value for auth_permission
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 32 WHERE name = 'auth_permission';

-- ----------------------------
-- Indexes structure for table auth_permission
-- ----------------------------
CREATE INDEX "auth_permission_content_type_id_2f476e4b"
ON "auth_permission" (
  "content_type_id" ASC
);
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq"
ON "auth_permission" (
  "content_type_id" ASC,
  "codename" ASC
);

-- ----------------------------
-- Auto increment value for auth_user
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 2 WHERE name = 'auth_user';

-- ----------------------------
-- Indexes structure for table auth_user_groups
-- ----------------------------
CREATE INDEX "auth_user_groups_group_id_97559544"
ON "auth_user_groups" (
  "group_id" ASC
);
CREATE INDEX "auth_user_groups_user_id_6a12ed8b"
ON "auth_user_groups" (
  "user_id" ASC
);
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq"
ON "auth_user_groups" (
  "user_id" ASC,
  "group_id" ASC
);

-- ----------------------------
-- Indexes structure for table auth_user_user_permissions
-- ----------------------------
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c"
ON "auth_user_user_permissions" (
  "permission_id" ASC
);
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b"
ON "auth_user_user_permissions" (
  "user_id" ASC
);
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq"
ON "auth_user_user_permissions" (
  "user_id" ASC,
  "permission_id" ASC
);

-- ----------------------------
-- Auto increment value for django_admin_log
-- ----------------------------

-- ----------------------------
-- Indexes structure for table django_admin_log
-- ----------------------------
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb"
ON "django_admin_log" (
  "content_type_id" ASC
);
CREATE INDEX "django_admin_log_user_id_c564eba6"
ON "django_admin_log" (
  "user_id" ASC
);

-- ----------------------------
-- Auto increment value for django_content_type
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 8 WHERE name = 'django_content_type';

-- ----------------------------
-- Indexes structure for table django_content_type
-- ----------------------------
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq"
ON "django_content_type" (
  "app_label" ASC,
  "model" ASC
);

-- ----------------------------
-- Auto increment value for django_migrations
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 20 WHERE name = 'django_migrations';

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "django_session_expire_date_a5c62663"
ON "django_session" (
  "expire_date" ASC
);

-- ----------------------------
-- Indexes structure for table home_mentaldisorder
-- ----------------------------
CREATE INDEX "home_mentaldisorder_user_id_23b30da6"
ON "home_mentaldisorder" (
  "user_id" ASC
);

-- ----------------------------
-- Auto increment value for home_userprofile
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 1 WHERE name = 'home_userprofile';

-- ----------------------------
-- Indexes structure for table home_userprofile
-- ----------------------------
CREATE INDEX "home_userprofile_user_id_d1f7b466"
ON "home_userprofile" (
  "user_id" ASC
);

PRAGMA foreign_keys = true;










CREATE TABLE medication_reminder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    medication_name TEXT NOT NULL,
    dosage TEXT,
    frequency TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    times_of_day TEXT,
    notes TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user (id)
);























-- StyleYoung Database Schema
-- Generated: 2025-08-28 00:47:46
-- SQLite3 Schema Export

CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);

CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

CREATE TABLE "usuarios_usuario" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "nombre" varchar(100) NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "direccion" varchar(255) NOT NULL, "telefono" varchar(15) NOT NULL);

CREATE TABLE "usuarios_usuario_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "usuario_id" bigint NOT NULL REFERENCES "usuarios_usuario" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "usuarios_usuario_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "usuario_id" bigint NOT NULL REFERENCES "usuarios_usuario" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "usuarios_usuario" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);

CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

CREATE TABLE "tienda_categoria" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(50) NOT NULL, "descripcion" text NOT NULL);

CREATE TABLE "tienda_carritocompras" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "total" decimal NOT NULL, "fecha_creacion" datetime NOT NULL, "activo" bool NOT NULL, "usuario_id" bigint NOT NULL REFERENCES "usuarios_usuario" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "tienda_pedido" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "total" decimal NOT NULL, "estado" varchar(20) NOT NULL, "fecha_pedido" datetime NOT NULL, "direccion_entrega" varchar(255) NOT NULL, "usuario_id" bigint NOT NULL REFERENCES "usuarios_usuario" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "tienda_talla" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "talla" varchar(10) NOT NULL, "stock" integer NOT NULL, "producto_id" bigint NOT NULL REFERENCES "tienda_producto" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "tienda_itempedido" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cantidad" integer NOT NULL, "precio_unitario" decimal NOT NULL, "pedido_id" bigint NOT NULL REFERENCES "tienda_pedido" ("id") DEFERRABLE INITIALLY DEFERRED, "producto_id" bigint NOT NULL REFERENCES "tienda_producto" ("id") DEFERRABLE INITIALLY DEFERRED, "talla_id" bigint NOT NULL REFERENCES "tienda_talla" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "tienda_itemcarrito" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cantidad" integer NOT NULL, "fecha_agregado" datetime NOT NULL, "carrito_id" bigint NOT NULL REFERENCES "tienda_carritocompras" ("id") DEFERRABLE INITIALLY DEFERRED, "producto_id" bigint NOT NULL REFERENCES "tienda_producto" ("id") DEFERRABLE INITIALLY DEFERRED, "talla_id" bigint NOT NULL REFERENCES "tienda_talla" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "tienda_producto" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(100) NOT NULL, "descripcion" text NOT NULL, "precio" decimal NOT NULL, "marca" varchar(50) NOT NULL, "color" varchar(30) NOT NULL, "material" varchar(50) NOT NULL, "fecha_creacion" datetime NOT NULL, "categoria_id" bigint NOT NULL REFERENCES "tienda_categoria" ("id") DEFERRABLE INITIALLY DEFERRED, "total_vendidos" integer NOT NULL);


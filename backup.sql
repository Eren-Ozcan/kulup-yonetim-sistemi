--
-- PostgreSQL database dump
-- Veritabanı yedeği alınmıştır. Bu yedek, veritabanı nesnelerinin ve verilerinin yeniden oluşturulmasını sağlar.
--

-- Veritabanı sürüm bilgisi
-- Yedeği alınan PostgreSQL sürümü: 15.10
-- pg_dump aracı kullanılarak yedek alındı.

-- Zaman aşımı, veri kodlaması ve diğer temel ayarları yapılandırıyoruz.
SET statement_timeout = 0;  -- Sorgu zaman aşımı süresi sınırını kaldırır.
SET lock_timeout = 0;  -- Kilit zaman aşımı süresi sınırını kaldırır.
SET idle_in_transaction_session_timeout = 0;  -- İşlem sırasında boş oturum zaman aşımı sınırını kaldırır.
SET client_encoding = 'UTF8';  -- İstemci karakter kodlamasını UTF-8 olarak ayarlar.
SET standard_conforming_strings = on;  -- Standartlara uygun dize ayarlaması.
SELECT pg_catalog.set_config('search_path', '', false);  -- Varsayılan arama yolunu temizler.
SET check_function_bodies = false;  -- Fonksiyon gövdelerindeki hataları kontrol etmeyi devre dışı bırakır.
SET xmloption = content;  -- XML seçeneğini içerik olarak ayarlar.
SET client_min_messages = warning;  -- Minimum istemci mesaj seviyesini uyarıya ayarlar.
SET row_security = off;  -- Satır güvenlik politikasını devre dışı bırakır.

SET default_tablespace = '';  -- Varsayılan tablo alanını ayarlar.
SET default_table_access_method = heap;  -- Varsayılan tablo erişim yöntemini yığın (heap) olarak belirler.

--
-- Tablo tanımlamaları başlıyor.
--

-- Bütçe tablosunun tanımlaması.
CREATE TABLE public.budget (
    id integer NOT NULL,  -- Birincil anahtar (otomatik artan)
    income_source character varying(255),  -- Gelir kaynağı (örneğin, sponsor, aidat)
    amount numeric(10,2) NOT NULL,  -- Tutar (maksimum 10 basamaklı, 2 ondalık basamak)
    date date NOT NULL  -- Gelir/gider tarihi
);

-- Bu tabloya ait sahiplik PostgreSQL kullanıcısına atanmıştır.
ALTER TABLE public.budget OWNER TO postgres;

-- budget tablosu için otomatik artan bir sıra (sequence) oluşturuluyor.
CREATE SEQUENCE public.budget_id_seq
    AS integer
    START WITH 1  -- İlk değer.
    INCREMENT BY 1  -- Her seferinde artış miktarı.
    NO MINVALUE  -- Minimum değer belirtilmemiş.
    NO MAXVALUE  -- Maksimum değer belirtilmemiş.
    CACHE 1;  -- Belleğe alınan sıra numarası.

-- budget_id_seq sahibi olarak PostgreSQL kullanıcısı atanıyor.
ALTER TABLE public.budget_id_seq OWNER TO postgres;

-- budget tablosundaki id sütunu için bu sıra (sequence) bağlanıyor.
ALTER SEQUENCE public.budget_id_seq OWNED BY public.budget.id;

-- Diğer tablolar için aynı yapılandırmalar devam ediyor...

--
-- Belgeler (documents) tablosunun tanımlaması.
--
CREATE TABLE public.documents (
    id integer NOT NULL,  -- Birincil anahtar.
    title character varying(255) NOT NULL,  -- Belge başlığı.
    content text NOT NULL,  -- Belgenin içeriği.
    upload_date date NOT NULL  -- Yükleme tarihi.
);

ALTER TABLE public.documents OWNER TO postgres;

-- documents tablosu için otomatik artan bir sıra oluşturuluyor.
CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.documents_id_seq OWNER TO postgres;
ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;

-- Etkinlikler (events) tablosunun tanımlaması.
CREATE TABLE public.events (
    id integer NOT NULL,  -- Birincil anahtar.
    title character varying(255) NOT NULL,  -- Etkinlik başlığı.
    description text NOT NULL,  -- Etkinlik açıklaması.
    event_date date NOT NULL  -- Etkinlik tarihi.
);

ALTER TABLE public.events OWNER TO postgres;

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.events_id_seq OWNER TO postgres;
ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;

-- Kullanıcılar (users) tablosunun tanımlaması.
CREATE TABLE public.users (
    id integer NOT NULL,  -- Birincil anahtar.
    email character varying(100) NOT NULL,  -- Kullanıcı e-posta adresi (benzersiz).
    username character varying(50) NOT NULL,  -- Kullanıcı adı.
    password character varying(200) NOT NULL,  -- Kullanıcı şifresi.
    role character varying(20) NOT NULL  -- Kullanıcı rolü (örneğin: admin, member).
);

ALTER TABLE public.users OWNER TO postgres;

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.users_id_seq OWNER TO postgres;
ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

-- Bütçe tablosu için varsayılan değerler atanıyor.
ALTER TABLE ONLY public.budget ALTER COLUMN id SET DEFAULT nextval('public.budget_id_seq'::regclass);

-- Diğer tablolar için de benzer şekilde varsayılan değerler atanıyor...

--
-- Tablo verileri ekleniyor.
--

-- budget tablosu için veri ekleme.
COPY public.budget (id, income_source, amount, date) FROM stdin;
1	Sponsorship	5000.00	2024-12-01
2	Membership Fees	1200.00	2024-12-15
\.

-- events tablosu için veri ekleme.
COPY public.events (id, title, description, event_date) FROM stdin;
1	Annual Meeting	Discuss club progress and future plans.	2024-12-31
3	123	21313	2000-11-11
\.

-- users tablosu için veri ekleme.
COPY public.users (id, email, username, password, role) FROM stdin;
1	admin@example.com	Admin User	123	admin
2	user1@example.com	User One	password1	member
3	user2@example.com	User Two	password2	member
\.

--
-- Sıra değerlerini güncelleme.
--

-- Sıralar, tabloların mevcut maksimum id değerine güncelleniyor.
SELECT pg_catalog.setval('public.budget_id_seq', 2, true);
SELECT pg_catalog.setval('public.documents_id_seq', 1, false);
SELECT pg_catalog.setval('public.events_id_seq', 3, true);
SELECT pg_catalog.setval('public.users_id_seq', 3, true);

--
-- Kısıtlamalar ekleniyor.
--

-- Birincil anahtarlar.
ALTER TABLE ONLY public.budget ADD CONSTRAINT budget_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.documents ADD CONSTRAINT documents_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.events ADD CONSTRAINT events_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);

-- E-posta benzersizliği.
ALTER TABLE ONLY public.users ADD CONSTRAINT users_email_key UNIQUE (email);

-- Yabancı anahtarlar.
ALTER TABLE ONLY public.members ADD CONSTRAINT members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);

--
-- Yedekleme tamamlandı.
--

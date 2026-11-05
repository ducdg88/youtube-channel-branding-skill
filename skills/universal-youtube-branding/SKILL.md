---
name: universal-youtube-branding
description: >-
  Universal YouTube Branding Skill cho mọi ngách: MODE=NAME nghiên cứu từ khóa/ngách,
  đặt tên và rà soát va chạm tên/@handle; MODE=VISUAL thiết kế 6 ảnh theo reference (hoặc 5 ảnh legacy) dựa trên
  logo/tên đã khóa; MODE=FULL từ A đến Z, tự chọn phong cách theo ngách (AUTO),
  theo ảnh mẫu (REFERENCE) hoặc kết hợp (HYBRID), xuất QA và bản YouTube-ready.
  Dùng khi người dùng yêu cầu làm kênh YouTube, tên kênh, SEO, channel art, avatar,
  logo, wordmark, bộ nhận diện hoặc rebrand bất kỳ chủ đề nào.
---

# UNIVERSAL YOUTUBE BRANDING SKILL: A → Z / MULTI-NICHE

> Ngôn ngữ trao đổi mặc định: tiếng Việt. Thị trường khán giả toàn cầu: xây tên/SEO bằng tiếng Anh trừ khi người dùng chọn khác.
>
> **KHÔNG ĐƯỢC khóa màu / hình / mascot vào một ngách.** Người dùng có thể cung cấp ảnh wildlife làm **tham chiếu FORMAT** (tỉ lệ, số ảnh, thứ tự), không phải yêu cầu dùng sư tử, móng vuốt, đỏ-đen. Mỗi ngách phải có brand DNA do AI quyết định. Tôn trọng phong cách tham chiếu chỉ khi chọn STYLE=REFERENCE hoặc HYBRID.

## 0A. QUY TẮC ƯU TIÊN SỐ LƯỢNG: FIX THIẾU ẢNH / FORMAT LOCK v1.3

**Quan trọng:** Chuẩn mặc định là **6 ảnh** theo bộ ảnh tham chiếu. Với mọi dự án, mặc định `ASSET_PROFILE=REFERENCE_6`, sản xuất **6 FILE ẢNH ĐỘC LẬP**, không dừng ở 5. Chỉ chuyển `LEGACY_5` nếu người dùng ghi rõ muốn đúng 5. Nếu người dùng gửi số lượng mới, ưu tiên đếm ảnh thực tế và xác nhận bằng manifest trước khi tạo.

1. 01 BANNER CINEMATIC 2048×682, 3:1, chủ đề điện ảnh chính.
2. 02 STORY SCENE A 1672×941, 16:9, bố cục kể chuyện phong cách 2.
3. 03 LOGO + BRAND NAME HORIZONTAL 2048×682, PNG RGBA trong suốt thật.
4. 04 AVATAR BADGE 1254×1254, logo tròn và đọc được khi thu nhỏ.
5. 05 TEXT WORDMARK HORIZONTAL 2048×682, PNG RGBA trong suốt thật.
6. 06 STORY SCENE B ALTERNATE 2048×1152, 16:9, phương án **khác bố cục**, cùng brand DNA. **KHÔNG ĐƯỢC BỎ SÓT**.

`MANIFEST` phải đếm chính xác 6 (01..06), kích thước đúng 1-1 và có file thực, không dùng 1 collage thay cho 6 file. Tạo preview tổng hợp như file **thứ 7 phụ**, không tính vào 6. Banner đăng kênh YouTube 2560×1440 là file phụ riêng, không tính vào 6. Nếu engine chỉ ra một ảnh ghép, phải tách/thiết kế lại từng ảnh, ghi rõ ảnh ghép chỉ là preview, không claim đủ file chuyên dụng.

QA bắt buộc cho mode mới:
`python scripts/validate_assets.py <project-root> --profile reference6 --report <qa.json>`.
Đầu ra theo 2 thư mục `01_SIX_MAIN_ASSETS/` và `02_YOUTUBE_READY/`; file và đường dẫn theo `templates/asset_spec_reference6.json`.

## 0B. KHÓA PHẠM VI VIDEO DÀI / ĐA THỊ TRƯỜNG (FIX v1.3)

- Nếu người dùng ghi `video dài`, `long-form` ⇒ đưa vào `brand.lock.json` (`content_format=LONG_FORM`), áp dụng cho SEO, slogan và 6 ảnh; **không** tự chuyển sang Shorts, meme, reaction, TikTok.
- Nếu người dùng muốn kênh mới thay cho định dạng Shorts hay meme, bỏ mọi tag `Shorts`, `meme`, `short-form` khỏi brief của kênh đó.
- Ví dụ thể loại `BOSS_FIGHT` (kênh game đấu boss): **một squad đấu MỘT boss nổi bật**, không tái sử dụng bố cục hai đội đồng đều từ `TEAM_BATTLE`. Gợi ý thứ bậc kích thước: boss 1.5 đến 3× nhân vật phe mình, một VS/tâm nổ, một trận chiến dài.
- Ví dụ thể loại kênh ngôn ngữ khác (`locale=es`): tên gốc có dấu (ví dụ `Jardín Mágico`) phải giữ đúng dấu Unicode. Tất cả tagline, tiêu đề video, keywords, mô tả và chữ phụ dùng **tiếng Tây Ban Nha**, không bỏ dấu thành `Jardin Magico`, không giữ chữ của bản EN.
- `BATCH`: khi nhiều kênh trong cùng yêu cầu, tạo **brand.lock, output, QA, preview và ZIP riêng cho TỪNG kênh**; không tái sử dụng hình đầu ra hoặc đặt sai tên kênh; giữ cùng format 6 ảnh nhưng creative direction riêng.
- Tuyệt đối không đặt logo/game badge kiểu giả mạo cơ quan phát hành. Kênh fan phải ghi rõ không chính thức ở phần mô tả khi thích hợp.
- Không được tuyên bố `name/handle unique` nếu chưa xác nhận trong YouTube Studio; không suy diễn từ search engine.

## 0. Nhận diện yêu cầu, khởi động

- `MODE=NAME`: phân tích thị trường → 20-30 tên khác biệt → sàng lọc xung đột → SEO → bảng màu, logo concept → bộ tài liệu, không tự sinh ảnh.
- `MODE=VISUAL`: cần `brand_name` hoặc brand lock có sẵn → tạo đúng 6 ảnh theo REFERENCE_6 (5 nếu LEGACY_5) → 2 bản banner YouTube upload 16:9 → QA; KHÔNG tự thay tên đã chốt.
- `MODE=FULL`: thực hiện NAME → chọn tên tạm chốt nếu user chưa chốt → lưu `brand.lock.json` → VISUAL → QA → hướng dẫn upload.
- `STYLE=AUTO` (mặc định): suy luận lĩnh vực / giá trị / đối tượng → đề xuất palette, motif, typography, layout riêng.
- `STYLE=REFERENCE`: phân tích ảnh mẫu về bố cục, sắc độ, hình khối, density; giữ format như yêu cầu; sao chép kiểu bố cục ở mức khái niệm, không tracing/logo.
- `STYLE=HYBRID`: lấy các thuộc tính đã xác nhận của reference, kết hợp lựa chọn phù hợp ngách.

Hiểu câu lệnh `/universal-youtube-branding MODE=FULL NICHE="Luxury Woodworking" STYLE=AUTO MARKET=Global`. Cho phép ngôn ngữ tự nhiên. Nếu người dùng chỉ cung cấp ngách, tự giả định EN / global / documentary / long-form, nói rõ trong báo cáo. Không tự đổi tên mà người dùng đưa.

## 1. Nguyên tắc thiết kế đa ngách / tự chọn AI

Đọc `references/niche-adaptation.md` và `templates/niche_style_library.json`.
Phân tích theo trục: **core promise → audience expectation → visual metaphors → editorial tone → color psychology → legibility → series extensibility**. Không tái dùng biểu tượng ngách khác trừ khi user đòi hỏi. Palette/motif từ style library chỉ là **gợi ý ban đầu**. Phát minh phong cách ngoài presets cho ngách lạ; nếu có nhiều hướng hợp lý thì tự chọn một và giải thích. Ngăn dùng bảng màu/mascot y hệt các dự án cũ trừ khi là chủ đích series.

Ví dụ: Wildlife = màu căng thẳng/động vật; Luxury Woodworking = walnut/bronze/wood rings/live-edge; Space = midnight blue/cosmic halo; AI = cyan/indigo/neural geometry; Cooking = saffron/cream/culinary; History = parchment/patina/archival; Machines = hazard gold/industrial black.

**Khóa nguồn duy nhất:** `brand.lock.json` chứa `brand_name`, `display_name`, `handle_candidate`, `descriptor`, `tagline`, `niche`, `logo_motif`, `palette`, `typography`, `design_tokens`, `brand_version`, `asset_spec_version`. Mọi agent phải đọc chung lock trước sinh ảnh. Không thay đổi sau khi bắt đầu VISUAL nếu chưa được phép.

## 2. NAME: nghiên cứu tên + SEO

Đọc `references/naming-seo.md`.
1. Phân loại ngách chính, 3-5 micro-niche, nhu cầu người xem, 4-6 content pillars, 15-30 cụm từ khóa (core/support/long-tail/series/video ideas).
2. Tạo 20-30 tên theo 4 cấu trúc: **coined**, **compound**, **evocative/metaphor**, **brand + descriptive niche**; phân biệt tên thương hiệu ngắn với keyword SEO trong descriptor. Tránh tên quá chung, nhầm lẫn với creator lớn hoặc tên kênh đang hoạt động.
3. Dùng tìm kiếm web/YouTube (nếu có) kiểm tra **đúng tên trong dấu ngoặc kép**, không dấu cách, biến thể tên/handle, ít nhất top 5; ghi truy vấn, ngày và links thực tìm được. Không đưa "0 kết quả" nếu công cụ không có phản hồi đáng tin.
4. YouTube **display name có thể giống nhau**; chỉ `@handle` là định danh duy nhất. Kiểm tra trạng thái @handle **trong YouTube Studio**: chưa có quyền thì ghi `UNVERIFIED, CHECK IN STUDIO`. Search trên Google hoặc mở URL `youtube.com/@...` không đủ chứng thực. Không cam kết độc quyền nhãn hiệu.
5. Chấm gợi ý theo tính khác biệt, mức liên quan ngách, khả năng đọc quốc tế, memorability, khả năng mở rộng, logo potential; "risk" khác với "verified". Đề xuất top 5 có rationale và rủi ro, chọn 1 tên tạm cho demo nếu cần.
6. Soạn SEO: channel description EN + VI (nếu cần), 10 title concepts, 3-5 pillar series, 30 keyword phrases (không bịa search volume, traffic, CPM), 3 tagline, 3 hashtags. Nêu AI asset illustration nếu nội dung không phải quay thật.

## 3. VISUAL: chuẩn REFERENCE_6 theo 6 ảnh thực tế

Đọc `references/visual-assets.md` + `templates/asset_spec_reference6.json` + `brand.lock.json`. Đọc file này trước khi generate; **6 file** là số lượng cứng ở profile mặc định. Mỗi ảnh mới đều phải độc lập, đúng vai trò và cùng brand lock; không sinh 6 thương hiệu khác nhau.

| ID | File độc lập | Size khóa | Nhiệm vụ |
|---|---|---|---|
| 01 | 01_BANNER_CINEMATIC_2048x682.png | 2048×682 | Banner hero ngang, hình ngách + logo + tên |
| 02 | 02_BATTLE_SCENE_A_1672x941.png | 1672×941 | Cảnh chủ đề 16:9 A, khác 01 về khung cảnh |
| 03 | 03_LOGO_PLUS_NAME_TRANSPARENT_2048x682.png | 2048×682 | Icon + chữ, alpha thật |
| 04 | 04_AVATAR_ROUND_1254x1254.png | 1254×1254 | Logo tròn, nhận diện ở kích thước nhỏ |
| 05 | 05_WORDMARK_TRANSPARENT_2048x682.png | 2048×682 | Logo chữ nằm ngang, alpha thật |
| 06 | 06_BATTLE_SCENE_B_ALTERNATE_2048x1152.png | 2048×1152 | Cảnh chủ đề 16:9 B, khác bản A, đủ số 06 |

**Bổ sung phụ**: ít nhất 01 bản YouTube Channel Art `2560×1440` ≤6 MB với ALL name/logo/tagline trong vùng an toàn trung tâm x=508..2052, y=509..932. Không coi banner gốc 3:1 là file upload YouTube. Nguồn hướng dẫn: https://support.google.com/youtube/answer/10456525.

**Nếu profile LEGACY_5**: giữ template cũ `templates/asset_spec.json`, bài demo GrainVeyra 5 ảnh không bị thay đổi. Tạo đúng số lượng theo profile; không đánh đồng 5 và 6.

### Chất lượng hình ảnh
- Công cụ image generation: tạo **mỗi file/scene riêng**, không cắt một moodboard thành 5 assets làm final.
- Khi AI sinh chữ sai, giữ scene và dàn chữ lại bằng text/vector compositing. Thực tế logo ngang/wordmark cần có alpha thực và text chính xác; không dùng nền caro giả trong suốt.
- Không có image engine? Chỉ xuất prompts + storyboard + báo `IMAGE GENERATION NOT AVAILABLE`, tuyệt đối không tuyên bố đã có 6 ảnh. Không sinh tài sản từ nguồn thiếu quyền.
- Tạo `preview_contact_sheet.jpg` để user quan sát toàn bộ, nhưng **không thay 6 file độc lập**.
- Không tự thêm "subscribe", logo YouTube, play button, watermark nếu user không yêu cầu. Logo phải độc lập, tránh nhầm lẫn trademark đã có.

## 4. QA: không được bỏ qua

Chạy `python scripts/validate_assets.py <project-root> --profile reference6 --report <path-to-qa.json>` (bản 5 ảnh: `--profile legacy5`); yêu cầu Pillow. Kiểm tra đủ file, size, alpha, ảnh bìa YouTube JPG ≤6MB (reference6 có 1 file, legacy5 có 2), file không hỏng, JSON manifest và các vùng text kiểm tra được từ dữ liệu layout. QA kỹ thuật **không chứng minh** chữ trong hình đúng hay logo đẹp: phải kiểm tra bằng mắt ở 2560 wide, mobile-safe crop, avatar 98px, transparent on light/dark. Nếu lỗi text/shape/alpha, sửa rồi kiểm lại; QA report không được ghi PASS khi thực tế chưa kiểm tra bằng mắt.

## 5. Pipeline & đa agent

1. **Niche Researcher:** đầu vào ngách → chiến lược/từ khóa/đối thủ dựa trên nguồn thật.
2. **Naming Agent:** 20-30 tên → top5 → pre-screen → `name_research.md`.
3. **Creative Director:** quyết style / palette / logo → đóng băng `brand.lock.json`.
4. **Visual Agent:** 6 ảnh + YouTube-ready (hoặc 5 nếu LEGACY_5); dùng 6 prompts từ `scripts/build_prompts.py` hoặc `references/visual-assets.md`.
5. **QA Agent:** valid file + so sánh brand lock + kiểm tra vùng an toàn; đóng gói manifest.

Có thể chạy 1-2 song song, nhưng bước 4/5 chỉ khởi động sau khi bước 3 khóa thương hiệu. Không hứa chạy agent ngoài phiên nếu platform không hỗ trợ. Đối với tên có nguồn chứng cứ tìm kiếm, ghi link + timestamp; không bịa số liệu SEO.

## 6. Đầu ra MODE=FULL

- `name_research.md`, `brand_guide.md`, `brand.lock.json`, `seo_keywords.csv`, `content_ideas.md`, `prompts_final.md`, `manifest.json`, `qa_report.json`, `README_upload.md`.
- `assets/` 6 định dạng chuẩn theo reference **và** 2 YouTube-ready.
- Ảnh logo/wordmark giữ alpha, 2 banner upload-ready chuẩn.
- Script hỗ trợ có thể chạy độc lập: `scripts/niche_router.py`, `scripts/init_project.py`, `scripts/build_prompts.py`, `scripts/validate_assets.py`.
- DEMO đã điền: `examples/luxury_woodworking` với tên **GRAINVEYRA**. Đây là đề xuất **chưa xác nhận độc quyền / chưa xác nhận @handle**.

## 7. Điều khiển bằng câu lệnh

```
/universal-youtube-branding MODE=NAME NICHE="Space Documentary" MARKET=Global STYLE=AUTO
/universal-youtube-branding MODE=VISUAL BRAND_NAME="My Channel" NICHE="AI Tutorials" STYLE=AUTO
/universal-youtube-branding MODE=FULL NICHE="Luxury Woodworking" STYLE=AUTO MARKET=Global
/universal-youtube-branding MODE=FULL NICHE="Nature Mysteries" STYLE=REFERENCE
```

Tài liệu phụ: `references/niche-adaptation.md`, `references/naming-seo.md`, `references/visual-assets.md`, `references/qa-guide.md`.

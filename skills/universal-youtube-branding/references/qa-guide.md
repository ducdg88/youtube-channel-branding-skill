# Universal YouTube Branding v1.3: QA kỹ thuật + duyệt hình ảnh

## REFERENCE_6 (mặc định)
Phải có **SÁU** file độc lập, đúng đường dẫn trong `templates/asset_spec_reference6.json`:
01 banner 2048×682; 02 scene A 1672×941; 03 logo + tên 2048×682 transparent PNG; 04 avatar tròn 1254×1254; 05 wordmark 2048×682 transparent PNG; 06 scene B 2048×1152. 02 và 06 khác bố cục; ảnh ghép/moodboard chỉ là preview phụ.

Thêm 01 banner YouTube 2560×1440 JPG ≤6 MiB, toàn bộ nội dung trọng yếu trong trung tâm x=508-2052, y=509-932. Logo trong suốt phải có vùng alpha=0 thực sự. Avatar phải rõ trên điện thoại.

Run `python scripts/validate_assets.py <project_root> --profile reference6 --report <qa_report.json>`.

Technical PASS chỉ xác nhận định dạng, đúng count/kích cỡ/alpha/tệp, **không** đảm bảo logo đẹp hoặc chữ đúng. Bắt buộc duyệt bằng mắt: chính tả và dấu của ngôn ngữ kênh, khác nhau giữa scene A/B, tên và bảng màu đồng bộ, không còn tên thương hiệu cũ, phần chữ nằm trong vùng an toàn, biểu tượng avatar đọc được khi thu nhỏ, không giả làm kênh chính thức của nhà phát hành game hay thương hiệu khác.

## LEGACY_5
Chỉ kích hoạt nếu user **nói rõ 5 ảnh**. Không được hạ từ 6 xuống 5 do ảnh 02/06 có cùng tỷ lệ 16:9.

## Ví dụ thể loại (chỉ áp khi kênh đúng thể loại đó)
**Kênh đấu boss:** video DÀI; đội phe mình vs MỘT boss ở vị trí nổi bật; có thể có nhân vật nền nhưng không thành 2 đội ngang nhau, không Shorts/meme.
**Kênh gameplay tiếng Tây Ban Nha:** video DÀI; tên trên logo giữ đúng dấu (ví dụ `Jardín Mágico`), SEO, mô tả, tiêu đề bằng tiếng Tây Ban Nha; tránh chữ tiếng Anh trên logo hay tagline, không gộp với kênh khác.

## Nhiều kênh cùng lúc
Mỗi channel 1 project dir + `brand.lock.json` riêng. Không dùng logo của dự án A trong ảnh B. Validate, xuất preview và ZIP riêng; có thể tạo ZIP tổng để lưu trữ.

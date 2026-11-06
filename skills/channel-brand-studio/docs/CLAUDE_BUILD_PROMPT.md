# PROMPT CHO CLAUDE / ANTIGRAVITY: SAO CHÉP NGUYÊN VĂN

Hãy đọc trọn gói `Channel Brand Studio v3.0`, đặc biệt `SKILL.md`, `docs/WORKFLOW.md`, `configs/defaults.json` và `scripts/studio.py`. Nhiệm vụ là nâng cấp/tích hợp công cụ thiết kế nhận diện thương hiệu YouTube vào repository website tôi cấp quyền, ở dạng white-label cho người dùng phổ thông.

QUY TẮC HÀNG ĐẦU: **MẶC ĐỊNH 10 PHƯƠNG ÁN DEMO riêng** (có chọn 1 đến 20). Mỗi phương án là **1 concept thương hiệu hoàn chỉnh về ý tưởng** (logo/icon, chữ tên kênh, bảng màu, phong cách, hình ảnh) và có ảnh xem trước độc lập. Đừng nhầm 10 concept demo với 6 ảnh thành phẩm.

Khách có thể (a) nhập tên kênh sẵn có, (b) yêu cầu AI gợi ý tên, (c) cung cấp ảnh/logo mẫu có quyền sử dụng. Hệ thống phải render preview thật bằng image provider khả dụng, xếp gallery có ảnh riêng, tên phong cách, so sánh, duyệt/chọn sửa/mix. Không tự chốt. Sau khi người dùng chọn mới mở phần **tùy biến đầu ra**: các asset logo, avatar, banner, wordmark, hình nền, v.v.; kích thước PX, tỷ lệ, alpha, các loại file. Có các preset CUSTOM/REFERENCE_MATCH/YOUTUBE_BASIC và REFERENCE_6 **tùy chọn**, không áp đặt đúng 6 ảnh. Khóa `brand.lock.json` sau duyệt; sản xuất file riêng; QA; gói ZIP.

Thực hiện trên repository được cấp quyền. Khảo sát framework, CI/CD, persistence và cơ chế auth/billing trước khi thay đổi. Triển khai thật code, trang wizard, mô hình job và retry, status, persistent selection, provider adapter, cost caps, QA, mockup, tests, docs. Không để API key frontend. Tách dữ liệu theo tài khoản, quyền truy cập, upload validity, privacy, logs, retention, licensing. Có giao diện responsive tiếng Việt, chuẩn bị locale khác.

Nếu chưa có provider / repo / quyền deploy, không tự nhận đã làm xong; hoàn thiện những phần có thể làm, báo rõ blockers và cách cấu hình. Đừng dùng dữ liệu thực từ dự án cũ để làm demo. Đừng tự truy cập production, thanh toán, công khai hoặc deploy khi chưa đủ quyền. Không hứa 100% tên kênh là duy nhất.

Báo cuối: thay đổi source, lệnh chạy, endpoint, test logs, screenshot, cấu hình chưa có, chất lượng image provider thực tế, trạng thái deployment. Chỉ đánh dấu COMPLETE khi có bằng chứng file và xác nhận duyệt.

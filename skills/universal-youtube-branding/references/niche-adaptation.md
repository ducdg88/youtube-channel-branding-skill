# ADAPTIVE BRAND ENGINE / TỰ CHỌN BỐI CẢNH

Mục tiêu: một skill, nhiều brand identity, tránh clone template.

**INPUTS:** niche, subniche, market, target audience, expected tone, format, preferred/forbidden motifs, constraints, reference images (optional).

**PROCESS:**
1. Xác định người xem muốn cảm giác gì: trust, drama, wonder, luxury, calm, authority, playful.
2. Trích 3-5 ẩn dụ HÌNH THÁI tự nhiên cho ngách. Luxury woodworking => grain rings, live edge, planing ribbon, rough log-to-table; wildlife => claw/paw/savanna; technology => circuit topology. Chọn MỘT motif chủ đạo không trùng ngách khác.
3. Chọn hệ màu 5 vai trò: background, surface, accent, highlight, text. Không chỉ chọn màu vì 'đẹp'; kiểm tra tương phản chữ trên ảnh video và avatar thu nhỏ.
4. Chọn 2 kiểu chữ: chủ đạo có cá tính, phụ dễ đọc; ưu tiên font có thể cài hợp pháp. Hạn chế copy wordmark hiện có.
5. Xây 'BRAND LOCK': name casing, descriptor, tagline, logo symbol geometry, stroke width, palette HEX, layout zones, content themes, no-go.
6. Tự kiểm tra chống lặp: nếu 2 ngách khác nhau mà ra chung mascot, cùng palette, cùng texture → reset style.

## Three style modes
- `AUTO`: AI tự chọn toàn bộ, không suy diễn style từ hình reference nếu hình chỉ để đo kích thước.
- `REFERENCE`: người dùng yêu cầu theo phong cách ảnh mẫu → rút ra đặc điểm PHONG CÁCH, không sao chép nhãn hiệu/text/bố cục pixel-perfect.
- `HYBRID`: giữ chiều dài banner/logo/safe area, kết hợp cảm xúc mẫu nhưng motif/color theo ngành.

## Test cases
- `Luxury Woodworking` → refined editorial + gold foil + walnut + ringed V + factory/craftsman; không dùng đỏ máu/sư tử.
- `Wildlife Documentary` → natural power + animal silhouettes / photoreal predator + sunset/pine/jungle, màu riêng.
- `Quantum AI` → typography geometric + graph nodes + cyan gradient, không dùng hình gỗ.
- `History & Empires` → archival maps, bronze engraving, textured parchment.
- `Home Baking` → warm cream, handwritten detail, rolling-pin/flour motif.
- `Heavy Equipment` → steel, construction grid, hazard yellow, dust/industrial lighting.

## Bad outcomes to reject
- 5 ảnh là 5 tên khác nhau.
- Lấy màu wildlife để làm woodworking chỉ vì file reference có sư tử.
- Copy brand của kênh khác.
- Prompt thay đổi spelling giữa ảnh.
- Hình thumbnail chứa chữ micro 4px khi hiển thị điện thoại.

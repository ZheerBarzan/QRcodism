from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode
import io
from qrcode.image.svg import SvgPathImage

@csrf_exempt
def generate_qr(request):
    if request.method == "POST":
        data = request.POST.get('data', '')
        mode = request.POST.get('mode', 'link')
        img_format = request.POST.get('format', 'png') # Get format (default to png)

        # ... (Keep the WiFi logic from previous step here) ...

        if not data:
            return HttpResponse("No data provided", status=400)

        # 1. Configure the factory based on format
        if img_format == 'svg':
            # Create SVG factory
            factory = SvgPathImage
            content_type = "image/svg+xml"
        else:
            # Default to PNG
            factory = None 
            content_type = "image/png"

        # 2. Generate QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)

        # 3. Make Image
        if factory:
            img = qr.make_image(image_factory=factory)
        else:
            img = qr.make_image(fill_color="black", back_color="white")

        # 4. Save to Buffer
        buffer = io.BytesIO()
        img.save(buffer)
        buffer.seek(0)

        return HttpResponse(buffer, content_type=content_type)

    return HttpResponse("Invalid request method", status=405)
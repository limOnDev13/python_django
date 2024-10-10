from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def upload_file(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("uploaded_file"):
        uploaded_file = request.FILES["uploaded_file"]
        if uploaded_file.size >= 1024 * 1024 * 2:  # 2 MB
            raise ValueError("Image size more than 2 Mb")

        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        print("Saved file", filename)

    return render(request, "uploadfile/upload-file.html")

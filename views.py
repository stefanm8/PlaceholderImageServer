from django.http import HttpResponse, HttpResponseBadRequest
from django import forms
from io import BytesIO
from PIL import Image, ImageDraw
import random
from django.core.cache import cache
import hashlib
from django.views.decorators.http import etag


class ImageForm(forms.Form):

    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)
    def generate(self, image_format='PNG'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = "{}.{}.{}".format(width, height, image_format)
        content = cache.get(key)
        if content is None:
            print ("newImage")
            random_col = random.randint(0,255)
            random_col1 = random.randint(0,255)
            image = Image.new('RGB', (width, height), color=(random_col1,random_col,random_col1))
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height-textheight)
                textleft = (width-textwidth)
                Red = random.randint(155,255)
                draw.text((textleft, texttop),text, fill=(Red,Red,50))
            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key,content, 60 * 60)
        else:
            print ("not new at all")
        return content



def generate_etag(request, width, height):
    content = "Placeholder: {} X {}".format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag)
def generate_Placeholder(request, width, height):
    form = ImageForm({'height': height, 'width':width})
    if form.is_valid():
        height = form.cleaned_data['height']
        width = form.cleaned_data['width']
        image = form.generate()

        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest("invalid image")
def index(request):
    return HttpResponseBadRequest('Invalid image size')

from odoo import models
import io
from PIL import Image

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _resize_image(self, image, max_width=800, max_height=800):
        image_stream = io.BytesIO(image)
        with Image.open(image_stream) as img:
            img.thumbnail((max_width, max_height))
            resized_stream = io.BytesIO()
            img.save(resized_stream, format=img.format)
            resized_stream.seek(0)
            return resized_stream.read()

    def _convert_image_to_webp(self, image):
        image_stream = io.BytesIO(image)
        with Image.open(image_stream) as img:
            webp_stream = io.BytesIO()
            img.save(webp_stream, format='WEBP')
            webp_stream.seek(0)
            return webp_stream.read()

    def write(self, vals):
        if 'image_1920' in vals:
            resized_image = self._resize_image(vals['image_1920'])
            vals['image_1920'] = self._convert_image_to_webp(resized_image)
        return super(ProductTemplate, self).write(vals)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def write(self, vals):
        if 'image_1920' in vals:
            template = self.env['product.template'].browse(self.product_tmpl_id.id)
            resized_image = template._resize_image(vals['image_1920'])
            vals['image_1920'] = template._convert_image_to_webp(resized_image)
        return super(ProductProduct, self).write(vals)

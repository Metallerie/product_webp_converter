from odoo import models
import io
from PIL import Image

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _convert_image_to_webp(self, image):
        image_stream = io.BytesIO(image)
        with Image.open(image_stream) as img:
            webp_stream = io.BytesIO()
            img.save(webp_stream, format='WEBP')
            webp_stream.seek(0)
            return webp_stream.read()

    def write(self, vals):
        if 'image_1920' in vals:
            vals['image_1920'] = self._convert_image_to_webp(vals['image_1920'])
        return super(ProductTemplate, self).write(vals)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def write(self, vals):
        if 'image_1920' in vals:
            template = self.env['product.template'].browse(self.product_tmpl_id.id)
            vals['image_1920'] = template._convert_image_to_webp(vals['image_1920'])
        return super(ProductProduct, self).write(vals)

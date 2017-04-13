from .configurer import ReviewsConfig
from adminconfig import register
default_app_config = 'reviews.apps.ReviewsConfig'

register(ReviewsConfig)
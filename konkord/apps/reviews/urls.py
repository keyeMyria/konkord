from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add-review$',
        views.add_review, name="reviewed_with_chains_add"),
    url(r'^all-reviews$', views.all_reviews, name="reviewed_with_chains_list"),
    url(r'^add-reply$', views.add_reply, name="reviewed_with_chains_add_reply"),
    url(r'^rating-review$', views.rating, name="reviewed_with_chains_rating"),
    url(
        r'^all-reviews-by-type$',
        views.all_reviews_by_type, name='all_reviews_by_type'),
    url(
        r'^site-reviews$',
        views.SiteReviewsView.as_view(),
        name='reviewed_with_chains_site_reviews'
    )
]

from django.urls import include, path


from . import views


app_name = 'public'

urlpatterns = [
    path(
        'company/<slug>/',
        include([
            path('', views.CompanyDetailView.as_view()),
            path('feedback/', views.CompanyFeedbackView.as_view()),
            path('categories/',
                include([
                    path('', views.CategoriesView.as_view()),
                    path('<id>/', views.ProductsView.as_view())
                ])
            )
        ])
    ),
    path(
        'user/',
        views.UserCompaniesView.as_view(),
        name='UserCompaniesData'
    )
]

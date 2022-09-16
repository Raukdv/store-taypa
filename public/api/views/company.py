from django.http import Http404
from rest_framework import response, status, views

from core.models import Company
from ..serializers.company import CompanySerializer, CompanyFeedbackSerializer


class CompanyDetailView(views.APIView):
    serializer_class = CompanySerializer

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        serializer = self.serializer_class(
            instance=self.object,
            context=self.get_serializer_context()
        )

        return response.Response(serializer.data)

    def get_object(self):
        try:
            return Company.objects.get(slug=self.kwargs['slug'])
        except (KeyError, TypeError, Company.DoesNotExist):
            raise Http404

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


class CompanyFeedbackView(views.APIView):
    serializer_class = CompanyFeedbackSerializer

    def get_company(self):
        try:
            slug = self.kwargs['slug']
            return Company.objects.get(slug=slug)
        except (KeyError, TypeError, Company.DoesNotExist):
            raise Http404

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def post(self, request, *args, **kwargs):
        company = self.get_company()

        serializer = self.serializer_class(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(company=company)

        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )
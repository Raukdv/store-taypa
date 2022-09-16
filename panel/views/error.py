from django.shortcuts import render

#400: peticion invalida
def pag_400_bad_request(request, exception):
    response = render(request, '400.html')
    response.status_code=400
    return response

#403: peticion prohibida
def pag_403_forbidden(request, exception):
    response = render(request, '403.html')
    response.status_code=403
    return response

#404: página no encontrada
def pag_404_not_found(request, exception):
    response = render(request, '404.html')
    response.status_code = 404
    return response

#500: error en el servidor
def pag_500_error_server(request):
    response = render(request, '500.html')
    response.status_code=500
    return response
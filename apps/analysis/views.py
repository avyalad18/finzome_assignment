from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.permissions import AllowAny
from .utils import *


# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class AnalysisView(APIView) :
    permission_classes = (AllowAny,)

    def post(self,request):
        response = {"status": "success", "errorcode": "", "reason": "", "result": "", "httpstatus": HTTP_200_OK}
        try:
            body = request.data
            file_data = body['file']
            allowed_extensions = ['csv', 'CSV']
            ext = str(file_data).lower().split('.')[-1]

            if len(file_data) <= 0 :
                response["status"] = "error"
                response["httpstatus"] = HTTP_400_BAD_REQUEST
                response["reason"] = "please upload file first"
                return Response(response,status=response['httpstatus'])
                
            
            elif ext not in allowed_extensions:
                response["status"] = "error"
                response["httpstatus"] = HTTP_400_BAD_REQUEST
                response["reason"] = "Only CSV files are allowed."
                return Response(response,status=response['httpstatus'])
              
            result = {}
            df = pd.read_csv(file_data)
            data = calDailyReturns(df)
            daily_volatility =calDailyVolatility(data)
            anuual_volatility = calAnnualizedVolatility(daily_volatility,data.shape[0])
            result["daily_returns"] = data.fillna(0).to_dict('records')
            result["daily_volatility"] = daily_volatility
            result["anuual_volatility"] = anuual_volatility

            response['result'] = result

        except Exception as e :
            response["status"] = "error"
            response["httpstatus"] = HTTP_500_INTERNAL_SERVER_ERROR
            response["reason"] = f"[Error] : {str(e)}"

        return Response(response,status=response['httpstatus'])
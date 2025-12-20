from django.urls import path
from . import views

app_name = 'fiscal'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_fiscal, name='dashboard'),
    
    # Configuração
    path('configuracao/', views.configuracao_fiscal, name='configuracao'),
    
    # Notas Fiscais
    path('notas/', views.lista_notas, name='lista_notas'),
    path('notas/<int:pk>/', views.detalhe_nota, name='detalhe_nota'),
    
    # Emissão
    path('emitir/nfce/', views.emitir_nfce, name='emitir_nfce'),
    path('emitir/nfce/<int:venda_id>/', views.emitir_nfce, name='emitir_nfce_venda'),
    path('emitir/nfe/', views.emitir_nfe, name='emitir_nfe'),
    path('emitir/nfe/<int:venda_id>/', views.emitir_nfe, name='emitir_nfe_venda'),
    
    # Ações
    path('notas/<int:pk>/cancelar/', views.cancelar_nota, name='cancelar_nota'),
    path('notas/<int:pk>/carta-correcao/', views.carta_correcao, name='carta_correcao'),
    path('notas/<int:pk>/enviar-email/', views.enviar_email, name='enviar_email'),
    path('notas/<int:pk>/danfe/', views.download_danfe, name='download_danfe'),
    path('notas/<int:pk>/xml/', views.download_xml, name='download_xml'),
    
    # Inutilização
    path('inutilizar/', views.inutilizar_numeracao, name='inutilizar'),
    
    # API
    path('api/emitir-nfce/', views.api_emitir_nfce, name='api_emitir_nfce'),
    path('api/consultar/<str:chave>/', views.api_consultar_nota, name='api_consultar_nota'),
]

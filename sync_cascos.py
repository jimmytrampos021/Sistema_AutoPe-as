from estoque.models import AmperagemBateria, Produto, EstoqueCasco
from django.db.models import Sum

baterias = Produto.objects.filter(
    amperagem_bateria__isnull=False, 
    ativo=True
).values('amperagem_bateria').annotate(total=Sum('estoque_atual'))

print('Sincronizando estoque de cascos...')

for b in baterias:
    amp_id = b['amperagem_bateria']
    total = b['total'] or 0
    estoque, created = EstoqueCasco.objects.update_or_create(
        amperagem_id=amp_id,
        defaults={'quantidade': total}
    )
    print(f'{estoque.amperagem.amperagem}: {total} unidades')

print('Concluido!')

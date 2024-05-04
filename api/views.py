from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.conf import settings
from hashlib import sha256

dynamodb = settings.DYNAMODB_CLIENT


@api_view(['GET'])
def echo(request):
    return HttpResponse(request.query_params['string'])


@api_view(['POST'])
@parser_classes([JSONParser])
def get_price(request):
    item = dynamodb.get_item(
        TableName="online-shop-items",
        Key={
            'item_id': {'S': request.data['itemId']}
        }
    )['Item']
    per_item_price = int(item['per_item_price']['N'])
    tax_rate = float(item['tax_rate']['N'])
    total_price_pre_tax = per_item_price * request.data['quantity']
    total_price_with_tax = round(total_price_pre_tax * (1 + tax_rate))

    return JsonResponse({
        'itemId': request.data['itemId'],
        'quantity': request.data['quantity'],
        "perItemPrice": per_item_price,
        "totalPricePreTax": total_price_pre_tax,
        "taxRate": tax_rate,
        "totalPriceWithTax": total_price_with_tax
    })


@api_view(['POST'])
@parser_classes([JSONParser])
def compute(request):
    request.data.sort()

    hash = bytearray()
    for i in range(len(request.data)):
        number_hash = bytearray(sha256(int.to_bytes(request.data[i])).digest())
        new_hash = hash + number_hash
        hash = sha256(new_hash).digest()

    return HttpResponse(hash.hex())


@api_view(['POST'])
@parser_classes([JSONParser])
def parse(request):
    search_string = request.query_params['searchString']

    for index, i in enumerate(request.data):
        if i == search_string:
            return HttpResponse(index)

    return HttpResponse(-1)


@api_view(['GET'])
def query(request):
    initial_primary_key = request.query_params['initialPrimaryKey']
    current_primary_key = initial_primary_key
    counter = 0
    while True:
        counter += 1
        response = dynamodb.get_item(
            TableName="round-trip-table",
            Key={
                'primary_key': {'S': current_primary_key}
            }
        )
        current_primary_key = response['Item']['next_primary_key']['S']
        if current_primary_key == initial_primary_key:
            break

    return HttpResponse(counter)

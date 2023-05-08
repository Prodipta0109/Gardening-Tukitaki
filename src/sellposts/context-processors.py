from .models import Sell_Post_Category


def get_all_sell_categories(request):
    sell_categories = Sell_Post_Category.objects.all()
    context = {
        "sell_categories": sell_categories
    }
    return context
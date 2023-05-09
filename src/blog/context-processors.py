from .models import Category,Sell_Post_Category


def get_all_categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return context

def get_all_sell_categories(request):
    sell_categories = Sell_Post_Category.objects.all()
    context = {
        "sell_categories": sell_categories
    }
    return context
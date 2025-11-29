from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        price_fields = ['price_excl_tax', 'price_incl_tax', 'tax']
        for field in price_fields:
            value = adapter.get(field)
            if value:
                value = value.replace('£', '').strip()
                adapter[field] = float(value)

        string_fields = ['category', 'product_type']
        for field in string_fields:
            value = adapter.get(field)
            if value:
                adapter[field] = value.lower().strip()

        description = adapter.get('description')
        if description:
            adapter['description'] = description.strip()

        num_reviews = adapter.get('num_reviews')
        if num_reviews:
            adapter['num_reviews'] = int(num_reviews)
        else:
            adapter['num_reviews'] = 0

        availability = adapter.get('availability')
        if availability:
            if '(' in availability:
                availability = availability.split('(')[1].split()[0]
                adapter['availability'] = int(availability)
            else:
                adapter['availability'] = 0

        stars = adapter.get('stars')
        if stars:
            adapter['stars'] = stars.lower()

        return item
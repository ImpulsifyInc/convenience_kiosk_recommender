# Convenience Kiosk Recommender

This project was build to support a company that provides a system for self-serve kiosks type convenience stores. These are mostly located in hotels. For these businesses, the store is not the primary business, but can be a big boost of additional revenue. Since operating the retail store is not neccesarily the core compentancy of the hotel management, whatever support can be given in running the store is highly valuable.

## Data

The data provided for this project is propriety, and is not included in this repository. For development purposes, a copy of at PostgreSQL was obtained locally and queried directly

## Recommender

The intial recommender was build to suggest what additional products the store should be carrying. Since space is often limited, particularly for refridgerated items, suggestion of which products to stop carrying is also provided. Because having a variety of product categories available is key for customer satistfaction in this industry, products are calculated on a per-category basis. Briefly,

1. Each hotel is clustered into groups of similar hotels.
2. The top selling products for that hotel in a particular category over a particular data range are calculated.
3. Top products for that cluster of hotels as well as nationally are also calculated.
4. If the hotel is not carrying a product in the top n products, then the missing product(s) are suggested. (n defaults to 5, but is a user-adjustable parameter should one desire more or fewer products in a particular category)
5. In order to accomodate space for new products, if the hotel is carrying products that are not in the top n, AND these products make of less than x% (defaults to 10%) of sales in that category, suggestions for products to remove are also given.

### Clustering

### Output

### App



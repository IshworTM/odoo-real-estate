{
    "name": "Real estate",
    "description": "A module for all your Real Estate needs.",
    "author": "Ishwor",
    "website": "https://www.facebook.com",
    "summary": "A very real estate model",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        
        "views/estate_property_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_inherited_model_views.xml",
        "views/client_action.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "estate/static/src/**/*.js",
            "estate/static/src/**/*.xml",
            "estate/static/src/**/*.scss",
        ]
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}

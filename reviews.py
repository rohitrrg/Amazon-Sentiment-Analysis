class Reviews:
    def __init__(self):
    
        self.reviews = {'smartphone':{'img_url': 'https://m.media-amazon.com/images/I/61+g6KrDXdL._UF1000,1000_QL80_.jpg',
                                      'title':'Samsung Galaxy S24',
                                      'price':'79,999',
                                      'reviews':["This smartphone is blazing fast and handles everything smoothly. The battery easily lasts a full day, even with heavy use. Camera quality is superb, especially in low light. Definitely worth every penny.",
                                                    "The phone heats up quickly even with normal usage. Battery drains fast, and the software feels unpolished. I expected better at this price point.",
                                                    "Excellent device! The AMOLED display is vibrant and responsive. Face unlock works like a charm. Only downside is the lack of a headphone jack, but otherwise it's perfect.",
                                                    "Worst phone I’ve ever bought. The touch screen lags, apps crash constantly, and the camera is below average. Regret this purchase.",
                                                    "It's okay. Not great, not terrible. The build feels premium, but performance isn't consistent. It’s decent for casual use but not ideal for gaming or multitasking.",
                                                    "Absolutely love this phone! It’s sleek, powerful, and the battery life is amazing. I've had no issues whatsoever, and the photos come out beautifully crisp.",
                                                    "Mediocre at best. The UI is cluttered and filled with bloatware. The camera takes good photos in daylight but struggles in low-light conditions. Not very user-friendly.",
                                                    "Good phone overall. The processor handles daily tasks with ease, and the display is stunning. Speakers are average, but for the price, it’s a solid deal.",
                                                    "Terrible experience. The phone stopped charging after a month. Customer support was unhelpful. Totally disappointed.",
                                                    "A complete package! Great design, excellent performance, clean UI, and regular software updates. Easily one of the best smartphones in this range."]
                        },
                        'wireless headphones': {'img_url':'https://in.jbl.com/dw/image/v2/BFND_PRD/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw77e1df72/01.JBL_Wave%20Beam%202_Product%20Image_Hero_Black.png?sw=535&sh=535',
                                                'title':'JBL wave Beam 2',
                                                'price':'3,999',
                                                'reviews':[ "Fantastic sound quality with deep bass and clear highs. Battery lasts over 20 hours and charges quickly. Super comfortable for long listening sessions.",
                                                            "Very uncomfortable to wear for more than 30 minutes. Also, there’s a constant buzzing noise in the left ear.",
                                                            "Best wireless headphones I’ve ever owned! The noise cancellation is excellent, and connectivity is seamless across devices.",
                                                            "Sound cuts off randomly during calls. The build feels cheap and flimsy. Wouldn’t recommend to anyone.",
                                                            "Average performance. Audio quality is decent, but the mic picks up a lot of background noise. Not ideal for meetings.",
                                                            "Superb value for the price. Great for gym and travel. They stay in place and the Bluetooth connection is rock solid.",
                                                            "The battery life is okay, but the sound profile is too flat for music lovers. Bass is almost non-existent.",
                                                            "Very balanced audio and sleek design. Pairs instantly and works well even at a distance. Only con is the lack of a carrying case.",
                                                            "Terrible product. One earbud stopped working after two days. Customer service never responded.",
                                                            "Incredible audio performance, premium build, and intuitive touch controls. These headphones are worth every rupee!"]
                        },
                        'Face Serum': {'img_url':'https://m.media-amazon.com/images/I/51fo5Cdx4YL._UF1000,1000_QL80_.jpg',
                                       'title': 'Minimalist Oil Control & Anti-Acne 10% Niacinamide Face Serum with Zinc',
                                       'price': '599',
                                       'reviews': ["This serum completely changed my skincare routine! My skin feels smoother, looks brighter, and the fine lines have reduced visibly.",
                                                    "Gave me breakouts after just two uses. I had high hopes, but it didn’t suit my skin at all.",
                                                    "Lightweight and non-greasy. Absorbs quickly and leaves a healthy glow. Great under makeup too.",
                                                    "Smells weird and leaves a sticky residue. Not impressed with the results after two weeks of use.",
                                                    "My dark spots faded significantly within a month of consistent use. Really happy with this purchase.",
                                                    "Did absolutely nothing for my skin. I used it every night for three weeks with no noticeable difference.",
                                                    "Love the texture and how soft my skin feels in the morning. It’s become a staple in my routine.",
                                                    "Packaging is nice but the pump stopped working in a week. The product itself is just average.",
                                                    "I’ve tried many serums, but this one gave me the most visible results in the shortest time.",
                                                    "Too expensive for what it delivers. Didn’t live up to the hype on social media."]
                        }}

    def get_review(self, product):
        
        return self.reviews[product]
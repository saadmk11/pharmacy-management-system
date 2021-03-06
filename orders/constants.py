PAYMENT_PENDING = 1
PAYMENT_CONFIRMED = 2
PAYMENT_CANCELED = 3

PAYMENT_STATUS_CHOICES = (
    (PAYMENT_PENDING, 'Pending'),
    (PAYMENT_CONFIRMED, 'Confirmed'),
    (PAYMENT_CANCELED, 'Canceled'),
)

ORDER_PENDING = 1
ORDER_CONFIRMED = 2
ORDER_CANCELED = 3

ORDER_STATUS_CHOICES = (
    (ORDER_PENDING, 'Pending'),
    (ORDER_CONFIRMED, 'Confirmed'),
    (ORDER_CANCELED, 'Canceled'),
)

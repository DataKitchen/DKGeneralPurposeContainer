#!/usr/bin/env python3

import argparse
import sys
import traceback

from dkutils.datakitchen_api.datakitchen_client import DataKitchenClient
from dkutils.constants import COMPLETED_SERVING


if __name__ == '__main__':
    description = 'Create and monitor a test order'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('username', help='DataKitchen platform username')
    parser.add_argument('password', help='DataKitchen platform password')
    parser.add_argument('kitchen', help='Kitchen where the order will be kicked off')
    parser.add_argument('recipe', help='Recipe name of the order being kicked off')
    parser.add_argument('variation', help='Variation name of the order being kicked off')
    parser.add_argument('image_tag', help='GPC docker image tag')
    
    args = parser.parse_args()

    try:
        client = DataKitchenClient(args.username, args.password)
        sleep_secs = 10
        duration_secs = 60*5
        orders_details = [
            {
                "kitchen": args.kitchen,
                "recipe": args.recipe,
                "variation": args.variation,
                "parameters": {
                    "gpc_image_tag": args.image_tag
                }
            }
        ]
        print(f'Submitting order run...')
        result = client.create_and_monitor_orders(
            orders_details, sleep_secs, duration_secs, max_concurrent=1, stop_on_error=True
        )

        completed_orders = result[0]
        active_orders = result[1]
        queued_orders = result[2]

        if len(active_orders) > 0:
            raise Exception(f'Test order {active_orders[0]["order_run_id"]} still active after max duration exceeded.')
        if len(queued_orders) > 0:
            raise Exception(f'Test order still queued after max duration exceeded.')
        if len(completed_orders) < 1:
            raise Exception(f'Test order was not kicked off.')

        order_details = completed_orders[0]
        if client.get_order_run_status(order_details['order_run_id']) != COMPLETED_SERVING:
            raise Exception(f'Test order run {order_details["order_run_id"]} failed.')

        print(f'Test order run {order_details["order_run_id"]} succeeded.')

    except KeyboardInterrupt:
        print('\nKilled by user')
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    sys.exit()


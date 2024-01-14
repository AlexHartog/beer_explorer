from .models import BeerCheckin
import pandas as pd
from pprint import pprint
from django.db.models import F, Q


class UserStats:
    def __init__(self):
        # Load checkins
        beer_checkins = BeerCheckin.objects.all().values(user_name=F("user__name"))

        beer_checkin_df = pd.DataFrame(list(beer_checkins.values()))
        # Find first beer checkins
        pprint(beer_checkin_df)
        first_beer_checkins = (
            beer_checkin_df.loc[:, ["beer_id", "date"]]
            .drop_duplicates()
            .reset_index(drop=True)
        )
        # Merge with checkins
        self.valid_beer_checkins = first_beer_checkins.merge(
            beer_checkin_df, on=["beer_id", "date"]
        )

        pass

    def get_unique_beers_per_user(self):
        return self.valid_beer_checkins.groupby("user_name").size()

    def get_stats(self):
        pprint(
            self.get_unique_beers_per_user()
            .reset_index(name="points")
            .to_dict("records")
        )
        return (
            self.get_unique_beers_per_user()
            .reset_index(name="points")
            .to_dict("records")
        )

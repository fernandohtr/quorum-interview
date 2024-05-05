import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from congress.models import Bill, Legislator, Vote, VoteResult


class Command(BaseCommand):
    help = "Collects data from csv files and adds it to the database"

    def handle(self, *args, **options):
        BASE_PATH = Path(__file__).parent.parent.parent
        csv_directory = os.path.join(BASE_PATH, "csvfiles")
        self.import_data_from_cvs(csv_directory)

    def import_data_from_cvs(self, directory):
        csv_files_ordered = self.get_csv_files_ordered(directory)

        update_functions = {
            "legislators": self.update_legislator,
            "bills": self.update_bill,
            "votes": self.update_vote,
            "vote": self.update_vote_result,
        }

        for file_name in csv_files_ordered:
            csv_path = os.path.join(directory, file_name)
            prefix = file_name.split("_")[0]
            update_function = update_functions[prefix]

            update_function(csv_path)

    def get_csv_files_ordered(self, directory):
        """
        In order for there to be a consistent insertion of data into the database
        - due to foreign keys - it is necessary that the creation of instances
        follows the order: Legislator, Bill, Vote and VoteResult.
        """
        list_dir = os.listdir(directory)

        csv_files = [file for file in list_dir if file.endswith(".csv")]
        desired_order = ["legislators", "bills", "votes", "vote"]
        sorted_list = sorted(csv_files, key=lambda x: desired_order.index(x.split("_")[0]))
        return sorted_list

    def update_legislator(self, csv_path):
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Legislator.objects.create(
                    id=row["id"],
                    name=row["name"],
                )

    def update_bill(self, csv_path):
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    Bill.objects.create(
                        id=row["id"],
                        title=row["title"],
                        sponsor=Legislator.objects.get(id=row["sponsor_id"]),
                    )
                except Legislator.DoesNotExist:
                    print(
                        f"[csv inconsistency] [bill id {row["id"]}] Does not exist Legislator with id: {row["sponsor_id"]}"
                    )
                    continue

    def update_vote(self, csv_path):
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    Vote.objects.create(
                        id=row["id"],
                        bill=Bill.objects.get(id=row["bill_id"]),
                    )
                except Bill.DoesNotExist:
                    print(f"[csv inconsistency] [vote id {row["id"]}] Does not exist Bill with id: {row["bill_id"]}")
                    continue

    def update_vote_result(self, csv_path):
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    VoteResult.objects.create(
                        id=row["id"],
                        legislator=Legislator.objects.get(id=row["legislator_id"]),
                        vote=Vote.objects.get(id=row["vote_id"]),
                        vote_type=row["vote_type"],
                    )
                except Vote.DoesNotExist:
                    print(
                        f"[csv inconsistency] [vote result id {row["id"]}] Does not exist Vote with id: {row["vote_id"]}"
                    )
                    continue

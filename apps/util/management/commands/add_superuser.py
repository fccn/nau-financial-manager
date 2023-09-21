from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand


class Command(BaseCommand):
    help = "Create a superuser with a default password"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--password", dest="password", default="admin", help="Specifies password.")

    def handle(self, *args, **options):
        username = options.get("username") or "admin"
        email = f"admin-{username}@admin.com"
        password = options.get("password") or "admin"
        password = password if password != username else "admin"
        database = options.get("database")

        try:
            user_data = self.UserModel._default_manager.db_manager(database).create_superuser(
                username=username, email=email, password=password
            )
        except Exception as e:
            self.stderr.write("Error creating superuser: {}".format(e))
            user_data = None

        if user_data:
            self.stdout.write(
                "Superuser created successfully \n username: {} \n password: {} \n email: {}".format(
                    username, password, email
                )
            )
        else:
            self.stdout.write("Superuser creation failed.")

class ConflictResolver:

    @staticmethod
    def resolve(result):

        subject = result["subject"]

        room = result["room"]

        # ------------------------------------------------
        # Rule 1
        # If a definite room already exists (CL-xx or 303),
        # then "DS Lab", "AI Lab", etc. belong to subject.
        # ------------------------------------------------

        if room.startswith("CL-") or room.isdigit():

            for lab in [
                "DS Lab",
                "AI Lab",
                "ML Lab",
                "DL Lab",
                "Programming Lab",
                "Networking Lab",
                "Cloud Lab",
                "Database Lab",
                "IoT Lab",
                "Embedded Lab",
                "VLSI Lab"
            ]:

                if room == lab:

                    room = ""

                    subject = (subject + " " + lab).strip()

                    break

        result["room"] = room
        result["subject"] = subject

        return result
class PodcastModel:
    @staticmethod
    def check_field_presence(song_metadata):
        try:
            if (song_metadata["duration"] and song_metadata["name"] and song_metadata["host"]):
                return True
        except KeyError:
            return False
    
    @staticmethod
    def check_duration(duration):
        if (isinstance(duration, int) and duration >= 0):
            return True
        return False
    
    @staticmethod
    def check_name(name):
        if (isinstance(name, str) and len(name) <= 100):
            return True
        return False

    @staticmethod
    def check_participants(participants):
        if (isinstance(participants, list) and len(participants) <= 10):
            if (0 < len(participants)):
                for p in participants:
                    if not PodcastModel.check_name(p):
                        # participant name is not string(<=100)
                        return False

            return True
        return False

    @staticmethod
    def validate(song_metadata):
        are_fields_present = PodcastModel.check_field_presence(song_metadata)
        if are_fields_present:
            if (
                PodcastModel.check_name(song_metadata["name"]) and 
                PodcastModel.check_name(song_metadata["host"]) and
                PodcastModel.check_duration(song_metadata["duration"])
            ):
                # check participants list if present
                try:
                    if PodcastModel.check_participants(song_metadata["participants"]):
                        pass
                    else:
                        return False
                except KeyError:
                    pass
                return True
        else:
            return False

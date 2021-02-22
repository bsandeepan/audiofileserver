class SongModel:
    @staticmethod
    def check_field_presence(song_metadata):
        try:
            if (song_metadata["duration"] and song_metadata["name"]):
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
    def validate(song_metadata):
        are_fields_present = SongModel.check_field_presence(song_metadata)
        if are_fields_present:
            if (
                SongModel.check_name(song_metadata["name"]) and 
                SongModel.check_duration(song_metadata["duration"])
            ):
                return True
        else:
            return False

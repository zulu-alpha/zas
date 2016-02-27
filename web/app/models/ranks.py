from .. import db


class Rank(db.Document):
    """ZA Ranks, including images, descriptions and TS references"""
    name = db.StringField(min_length=4, max_length=25, unique=True, required=True)
    name_short = db.StringField(min_length=2, max_length=5, unique=True, required=True)
    description = db.StringField(min_length=2, max_length=200, unique=True, required=True)
    order = db.IntField(required=True)
    ts_group = db.IntField(required=True)
    image = db.FileField()
    image_squad = db.FileField()

    @classmethod
    def all(cls):
        """Returns all ranks by their 'order' attribute"""
        return cls.objects.order_by('order').all()

    @classmethod
    def by_name_short(cls, name_short):
        """Returns the Rank object that has the given short name

        :param name_short: String representing name_short attribute of a rank
        :return: Rank object
        """
        return cls.objects(name_short=name_short).first()

    @classmethod
    def image_by_id(cls, id):
        """Returns the image object by it's ID

        :param name_short: String representing of ID
        :return: image object or None
        """
        for rank in Rank.objects:
            if str(rank.image_squad.grid_id) == id:
                return rank.image_squad
            if str(rank.image.grid_id) == id:
                return rank.image

    @classmethod
    def create(cls, name, name_short, description, order, ts_group, image, image_squad):
        """Create a new rank

        :param name: String of the rank name
        :param name_short: String of the rank short name
        :param description: String of description of the rank
        :param order: Int of rank priority
        :param ts_group: Int of TS server group
        :param image: PNG Image of 512x512
        :param image_squad: PAA image for the Squad XML
        :return: BOOL if the DB was changed
        """
        rank = cls(
            name=name,
            name_short=name_short,
            description=description,
            order=int(order),
            ts_group=int(ts_group),
        )
        rank.image.put(image, content_type='image/png')
        rank.image_squad.put(image_squad, content_type='image/paa')
        rank.save()

        return True

    @classmethod
    def select_field_ranks(cls, blank=False, exclude=''):
        """Returns a list of tuples representing all ranks, identified by their name_short.
        This is useful for assigning a rank to a member.

        :param blank: Whether to make the first tuple an empty value (default: False)
        :param exclude: Rank by short name to exclude from the list
        :return: Tuple of format (rank.name_short, rank.name)
        """
        ranks = cls.objects.only('name_short', 'name', 'order').order_by('order').all()

        rank_choices = []
        for rank in ranks:
            if rank.name_short != exclude:
                rank_choices.append((rank.name_short, rank.name))

        if blank and not exclude == '':
            rank_choices.insert(0, ('', ''))

        return rank_choices

    def edit(self, name, name_short, description, order, ts_group, image, image_squad):
        """Create a new rank

        :param name: String of the rank name
        :param name_short: String of the rank short name
        :param description: String of description of the rank
        :param order: Int of rank priority
        :param ts_group: Int of TS server group
        :param image: PNG Image of 512x512
        :param image_squad: PAA image for the Squad XML
        :return: BOOL if the DB was changed
        """
        change = False
        if name and self.name != name:
            self.name = name
            change = True
        if name_short and self.name_short != name_short:
            self.name_short = name_short
            change = True
        if description and self.description != description:
            self.description = description
            change = True
        if order and self.order != order:
            self.order = order
            change = True
        if ts_group and self.ts_group != ts_group:
            self.ts_group = ts_group
            change = True
        if image:
            self.image.replace(image, content_type='image/png')
            change = True
        if image_squad:
            self.image_squad.replace(image_squad, content_type='image/paa')
            change = True

        if change:
            self.save()
            return True

        return False

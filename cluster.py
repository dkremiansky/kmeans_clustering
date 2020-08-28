from point import Point


class Cluster:
    def __init__(self, cluster_id, initial_point):
        self.id = cluster_id
        self._centroid = Point(str(cluster_id) + '_center')
        # IMPORTANT NOTE: data type of _points changed from dict to list because of name issues
        self._points = [initial_point]   # List of Point object
        self.compute_centroid()

    def compute_centroid(self):
        """
        Function to recompute new centroid of current points
        :return: Boolean value showing if centroid changed
        """
        if not self._points:
            print("Can't compute center without points")
            return

        # Saving old state
        old_centroid = tuple(self._centroid.coordinates)

        # We set new center as vector of zeroes. Length of the vector depends on number of coordinates
        number_of_coordinates = len(self._points[0].coordinates)
        new_coordinates = [0] * number_of_coordinates

        # Find median and set it as the new centroid
        new_coordinates = self.count_median(number_of_coordinates)
        self._centroid.set_coordinates(new_coordinates)

        is_changed = (old_centroid != tuple(self._centroid.coordinates))
        return int(is_changed)

    # Count the median of each coordinate of the new coordinates
    def count_median(self, number_of_coordinates):
        new_coordinate = [0]*number_of_coordinates
        for j in range(number_of_coordinates):
            i = 0
            median_index = 0
            temp_array = [0] * len(self._points)
            for point in self._points:
                temp_array[i] = point.coordinates[j]
                i = i + 1
            temp_array = sorted(temp_array)
            if (i % 2) == 0:
                median_index = int(i / 2) - 1
                median_coordinate = (temp_array[median_index] + temp_array[median_index + 1]) / 2
            else:
                median_index = int(i / 2)
                median_coordinate = temp_array[median_index]
            new_coordinate[j] = median_coordinate
        return new_coordinate

    def add_point(self, point):
        """
        Add point to the cluster
        :param point: Point to add
        """
        self._points.append(point)

    def remove_point(self, point=None):
        """
        Remove given point from the cluster. If point isn't provided then cluster is cleared.
        :param point: Point to remove or nothing
        """
        if not point:
            self._points = []
        elif point not in self._points:
            print('Point with name {} does not belong to cluster {}'.format(point.name, self.id))
        else:
            self._points.remove(point)

    def print(self):
        print('############################################')
        print('Cluster:', self.id)
        print('Number of points:', len(self._points))
        print('Centroid:', self._centroid.coordinates)
        print('Points:', ' '.join(sorted(x.name for x in self._points)))

    def compute_loss(self):
        distances = [self._centroid.distance_to(point.coordinates) for point in self._points]
        return sum(distances)

    def compute_SSE(self):
        errors = [self._centroid.distance_to(point.coordinates)**2 for point in self._points]
        return sum(errors)

    @property
    def centroid(self):
        return self._centroid.coordinates

    @property
    def number_of_points(self):
        return len(self._points)

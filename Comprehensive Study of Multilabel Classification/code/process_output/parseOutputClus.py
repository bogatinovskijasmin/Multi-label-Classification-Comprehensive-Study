def get_prediction_true_values(prediction_file, targetIndex):
    attributes = 0
    has_key = 0
    with open(prediction_file) as f:
        for l in f:
            if l.lower().startswith("@data"):
                break
            elif l.lower().startswith("@attribute"):
                attributes += 1
                if l.lower().strip().endswith("key"):
                    has_key = 1
        targets = (attributes - 1 - has_key) // targetIndex
        if targetIndex * targets + 1 + has_key != attributes:
            print(prediction_file)
            raise ValueError
        true_values_predictions = [[], []]
        for l in f:
            if not l.startswith('! Fold'):
                values = l.split(',')
                for i in range(targetIndex):
                    true_values_predictions[i].append([float(t) for t in values[i * targets + has_key:(i + 1) * targets + has_key]])
        return true_values_predictions

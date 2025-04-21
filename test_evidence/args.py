import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dataset",
    type=str,
    default="hover",
    help="specify dataset [hover, feverous]",
)

parser.add_argument(
    "--hover_num_hop",
    type=int,
    default=2,
    help="number of hops [two, three, four]",
)
parser.add_argument('--num_retrieved', default=1, type=int)
parser.add_argument('--max_evidence_length', default=3000, help = 'to avoid exceeding GPU memory', type=int)
parser.add_argument('--index', default=0, help = 'to see the exact data', type=int)

parser.add_argument(
    "--feverous_challenge",
    type=str,
    default="reasoning",
    help="type of challenge [reasoning, numerical, table]",
)
parser.add_argument("--version", type=str, default="V1.0", help="specify version")

parser.add_argument(
    "--model",
    type=str,
    default="gpt-3.5-turbo",
)
parser.add_argument(
    "--device_map",
    type=str,
    default="auto",
    help="specify device map [auto, balanced, balanced_low_0, sequential]",
)
parser.add_argument(
    "--temperature", type=float, default=0.7, help="temperature for GPT-3.5"
)
parser.add_argument(
    "--max_token", type=int, default=4096, help="specify number of max new token"
)

parser.add_argument(
    "--num_eval_samples", type=int, default=-1, help="specify number of evluating samples"
)
parser.add_argument(
    "--num_workers", type=int, default=10, help="specify number of workers"
)

args = parser.parse_args()

print(args)
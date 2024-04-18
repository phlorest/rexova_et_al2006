import itertools
import pathlib

import phlorest


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "rexova_et_al2006"

    def cmd_makecldf(self, args):
        self.init(args)
        
        # Add summary tree (e.g. MCCT or Consensus)
        summary = self.raw_dir.read_tree('data.nex.con.tre', detranslate=True)
        args.writer.add_summary(summary, self.metadata, args.log)

        # Add posterior tree distribution
        # each posterior has 131 trees, so remove 81 and take the last 50 from each
        args.writer.add_posterior(
            itertools.chain(
                self.raw_dir.read_trees('data.nex.run1.t', burnin=81, detranslate=True),
                self.raw_dir.read_trees('data.nex.run2.t', burnin=81, detranslate=True)
            ),
            self.metadata,
            args.log,
            rooted=True)
        
        # Add nexus data
        data = self.raw_dir.read_nexus('data.nex')
        args.writer.add_data(data, self.characters, args.log)
